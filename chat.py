# -*- coding: utf-8 -*-

import asyncio
import enum
import json
import logging
import time
from typing import *

import aiohttp
import tornado.websocket

import blivedm.blivedm as blivedm

logger = logging.getLogger(__name__)


class Command(enum.IntEnum):
    JOIN_ROOM = 0
    ADD_TEXT = 1
    ADD_GIFT = 2
    ADD_VIP = 3


http_session = aiohttp.ClientSession()
_avatar_url_cache: Dict[int, str] = {}


async def get_avatar_url(user_id):
    if user_id in _avatar_url_cache:
        return _avatar_url_cache[user_id]
    async with http_session.get('https://api.bilibili.com/x/space/acc/info',
                                params={'mid': user_id}) as r:
        data = await r.json()
    url = data['data']['face']
    if not url.endswith('noface.gif'):
        url += '@24w_24h.webp'
    _avatar_url_cache[user_id] = url

    if len(_avatar_url_cache) > 10000:
        for _, key in zip(range(100), _avatar_url_cache):
            del _avatar_url_cache[key]

    return url


class Room(blivedm.BLiveClient):
    _COMMAND_HANDLERS = blivedm.BLiveClient._COMMAND_HANDLERS.copy()

    def __init__(self, room_id):
        super().__init__(room_id, session=http_session)
        self.future = None
        self.clients: List['ChatHandler'] = []
        self.owner_id = None

    def start(self):
        self.future = self.run()

    def stop(self):
        if self.future is not None:
            self.future.cancel()
        asyncio.ensure_future(self.close())

    async def _get_room_id(self):
        """重载用来获取主播UID"""
        async with self._session.get(blivedm.ROOM_INIT_URL,
                                     params={'id': self._short_id},
                                     ssl=self._ssl) as res:
            if res.status == 200:
                data = await res.json()
                if data['code'] == 0:
                    self._room_id = data['data']['room_id']
                    self.owner_id = data['data']['uid']
                else:
                    raise ConnectionAbortedError('获取房间ID失败：' + data['msg'])
            else:
                raise ConnectionAbortedError('获取房间ID失败：' + res.reason)

    def send_message(self, cmd, data):
        body = json.dumps({'cmd': cmd, 'data': data})
        for client in self.clients:
            client.write_message(body)

    async def __my_on_get_danmaku(self, command):
        if command['info'][2][0] == self.owner_id:
            author_type = 3  # 主播
        elif command['info'][2][2] != 0:
            author_type = 2  # 房管
        elif command['info'][7] != 0:  # 1总督，2提督，3舰长
            author_type = 1  # 舰队
        else:
            author_type = 0
        self.send_message(Command.ADD_TEXT, {
            'avatarUrl': await get_avatar_url(command['info'][2][0]),
            'timestamp': command['info'][0][4],
            'authorName': command['info'][2][1],
            'authorType': author_type,
            'content': command['info'][1]
        })

    _COMMAND_HANDLERS['DANMU_MSG'] = __my_on_get_danmaku

    async def __my_on_gift(self, command):
        if command['data']['coin_type'] != 'gold':  # 丢人
            return
        self.send_message(Command.ADD_GIFT, {
            'avatarUrl': await get_avatar_url(command['data']['uid']),
            'authorName': command['data']['uname'],
            'giftName': command['data']['giftName'],
            'giftNum': command['data']['num'],
            'totalCoin': command['data']['total_coin']
        })

    _COMMAND_HANDLERS['SEND_GIFT'] = __my_on_gift

    async def __on_new_member(self, command):
        # 新舰长 {'cmd': 'GUARD_BUY', 'data': {'uid': 1822222, 'username': 'MRSKING', 'guard_level': 3,
        # 'num': 1, 'price': 198000, 'gift_id': 10003, 'gift_name': '舰长', 'start_time': 1558506165,
        # 'end_time': 1558506165}}
        self.send_message(Command.ADD_VIP, {
            'avatarUrl':  await get_avatar_url(command['data']['uid']),
            'authorName': command['data']['username'],
        })

    _COMMAND_HANDLERS['GUARD_BUY'] = __on_new_member


class RoomManager:
    def __init__(self):
        self._rooms: Dict[int, Room] = {}

    def add_client(self, room_id, client):
        if room_id in self._rooms:
            room = self._rooms[room_id]
        else:
            logger.info('创建房间%d', room_id)
            room = Room(room_id)
            self._rooms[room_id] = room
            room.start()
        room.clients.append(client)

        # 测试用
        # self.__send_test_message(room)

    def del_client(self, room_id, client: 'ChatHandler'):
        if room_id not in self._rooms:
            return
        room = self._rooms[room_id]
        room.clients.remove(client)
        if not room.clients:
            logger.info('移除房间%d', room_id)
            room.stop()
            del self._rooms[room_id]

    # 测试用
    @staticmethod
    def __send_test_message(room):
        room.send_message(Command.ADD_TEXT, {
            'avatarUrl': 'https://i0.hdslb.com/bfs/face/29b6be8aa611e70a3d3ac219cdaf5e72b604f2de.jpg@24w_24h.webp',
            'timestamp': time.time(),
            'authorName': 'xfgryujk',
            'authorType': 0,
            'content': '我能吞下玻璃而不伤身体'
        })
        room.send_message(Command.ADD_TEXT, {
            'avatarUrl': 'https://i0.hdslb.com/bfs/face/29b6be8aa611e70a3d3ac219cdaf5e72b604f2de.jpg@24w_24h.webp',
            'timestamp': time.time(),
            'authorName': '主播',
            'authorType': 3,
            'content': "I can eat glass, it doesn't hurt me."
        })
        room.send_message(Command.ADD_VIP, {
            'avatarUrl': 'https://i0.hdslb.com/bfs/face/29b6be8aa611e70a3d3ac219cdaf5e72b604f2de.jpg@24w_24h.webp',
            'authorName': 'xfgryujk',
        })
        room.send_message(Command.ADD_GIFT, {
            'avatarUrl': 'https://i0.hdslb.com/bfs/face/29b6be8aa611e70a3d3ac219cdaf5e72b604f2de.jpg@24w_24h.webp',
            'authorName': 'xfgryujk',
            'giftName': '礼花',
            'giftNum': 1,
            'totalCoin': 28000
        })
        room.send_message(Command.ADD_GIFT, {
            'avatarUrl': 'https://i0.hdslb.com/bfs/face/29b6be8aa611e70a3d3ac219cdaf5e72b604f2de.jpg@24w_24h.webp',
            'authorName': 'xfgryujk',
            'giftName': '节奏风暴',
            'giftNum': 1,
            'totalCoin': 100000
        })
        room.send_message(Command.ADD_GIFT, {
            'avatarUrl': 'https://i0.hdslb.com/bfs/face/29b6be8aa611e70a3d3ac219cdaf5e72b604f2de.jpg@24w_24h.webp',
            'authorName': 'xfgryujk',
            'giftName': '摩天大楼',
            'giftNum': 1,
            'totalCoin': 450000
        })
        room.send_message(Command.ADD_GIFT, {
            'avatarUrl': 'https://i0.hdslb.com/bfs/face/29b6be8aa611e70a3d3ac219cdaf5e72b604f2de.jpg@24w_24h.webp',
            'authorName': 'xfgryujk',
            'giftName': '小电视飞船',
            'giftNum': 1,
            'totalCoin': 1245000
        })


room_manager = RoomManager()


# noinspection PyAbstractClass
class ChatHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = None

    def open(self):
        logger.info('Websocket连接 %s', self.request.remote_ip)

    def on_message(self, message):
        if self.room_id is not None:
            return
        body = json.loads(message)
        if body['cmd'] == Command.JOIN_ROOM:
            self.room_id = int(body['data']['roomId'])
            logger.info('客户端%s加入房间%d', self.request.remote_ip, self.room_id)
            room_manager.add_client(self.room_id, self)
        else:
            logger.warning('未知的命令: %s data: %s', body['cmd'], body['data'])

    def on_close(self):
        logger.info('Websocket断开 %s room: %s', self.request.remote_ip, self.room_id)
        if self.room_id is not None:
            room_manager.del_client(self.room_id, self)

    # 测试用
    # def check_origin(self, origin):
    #     return True