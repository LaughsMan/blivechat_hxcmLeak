<template>
  <div>
    <el-form label-width="150px" size="mini">
      <h3>样式选择</h3>
      <table id="hxcmlist">
        <tr :key="style.name" v-for="style in styles">
          <td><img :src=style.preview /></td>
          <td>{{ style.name}}</td>
          <td class="btn"><a @click="loadCSS(style.name)">加载</a></td>
        </tr>
      </table>

    </el-form>
  </div>
</template>

<style>
#hxcmlist,
#hxcmlist tr {
  width: 100%;
}

#hxcmlist tr img {
  width: 320px;
}

#hxcmlist tr .btn {
  width: 40px;
}
</style>

<script>
import _ from 'lodash'
import * as common from './common'
import { mergeConfig } from '@/utils'
import hxcmLeak from '@/loader'


export const DEFAULT_CONFIG = {
  danmakuAtBottom: false,
  tickerAtButtom: false,

  showAvatars: true,
  avatarSize: 40,

  showUserNames: true,
  userNameFont: 'Noto Sans SC',
  userNameFontSize: 20,
  userNameLineHeight: 0,
  randomUserNamesColor: false,
  userNameColor: '#cccccc',
  ownerUserNameColor: '#ffd600',
  moderatorUserNameColor: '#5e84f1',
  memberUserNameColor: '#0f9d58',
  showBadges: true,
  badgesSize: 20,

  showMedal: true,
  showOnlyOwnerMedal: true,
  showMedalName: true,
  showMedalLevel: true,
  medalFontSize: 14,
  medalLineHeight: 0,

  messageFont: 'Noto Sans SC',
  messageFontSize: 18,
  messageLineHeight: 0,
  messageColor: '#000000',
  messageMergeSameUser: false,
  messageGroupBlockPadding: 0,

  emoticonSize: 48,
  emoticonInlineBorderRadius: 0,
  emoticonBlockBorderRadius: 4,

  showTime: false,
  showTimeRight: true,
  timeFont: 'Noto Sans SC',
  timeFontSize: 16,
  timeLineHeight: 0,
  timeColor: '#999999',

  bgColor: 'rgba(0, 0, 0, 0)',
  messageBgColor: '#ffffff',
  ownerMessageBgColor: 'rgba(231, 199, 30, 1)',
  moderatorMessageBgColor: 'rgba(41, 95, 251, 1)',
  memberMessageBgColor: 'rgba(43, 234, 43, 1)',

  firstLineFont: 'Noto Sans SC',
  firstLineFontSize: 20,
  firstLineLineHeight: 0,
  secondLineFont: 'Noto Sans SC',
  secondLineFontSize: 18,
  secondLineLineHeight: 0,
  scContentFont: 'Noto Sans SC',
  scContentFontSize: 18,
  scContentLineHeight: 0,
  showScTicker: false,
  showOtherThings: true,

  animateIn: true,
  fadeInTime: 200, // ms
  animateOut: false,
  animateOutWaitTime: 30, // s
  fadeOutTime: 200, // ms
  slide: true,
  reverseSlide: false
}

export default {
  name: 'hxcm',
  components: {
  },
  props: {
    value: String
  },
  data() {
    return {
      form: this.loadConfig(),
      filterText: '',
      tester: [{
        id: 1,
        label: '一级 1',
        children: [{
          id: 4,
          label: '二级 1-1',
          children: [{
            id: 9,
            label: '三级 1-1-1'
          }, {
            id: 10,
            label: '三级 1-1-2'
          }]
        }]
      }, {
        id: 2,
        label: '一级 2',
        children: [{
          id: 5,
          label: '二级 2-1'
        }, {
          id: 6,
          label: '二级 2-2'
        }]
      }, {
        id: 3,
        label: '一级 3',
        children: [{
          id: 7,
          label: '二级 3-1'
        }, {
          id: 8,
          label: '二级 3-2'
        }]
      }],
      styles: hxcmLeak.array(),
      defaultProps: {
        children: 'children',
        label: 'label'
      }
    }
  },
  computed: {
    result() {
      return `${this.importStyle}

${common.COMMON_STYLE}

${this.globalStyle}

${this.paddingStyle}

${this.avatarStyle}

${this.userNameStyle}

${this.messageStyle}

${this.timeStyle}

${this.backgroundStyle}

${this.scAndNewMemberStyle}

${this.animationStyle}
`
    },
    importStyle(name) {
      return ""
      // hxcmLeak.list.get(name)
    },
    globalStyle() {
      return `/* Global Setting */
yt-live-chat-renderer {
  ${this.form.tickerAtButtom ? `flex-direction: column-reverse;` : ''}
}
#item-scroller {
  ${this.form.danmakuAtBottom ? `display: flex;
  flex-direction: column;
  justify-content: flex-end;` : ''}
}`
    },
    paddingStyle() {
      return `/* Reduce side padding */
yt-live-chat-text-message-renderer {
  padding-left: 4px !important;
  padding-right: 4px !important;
}`
    },
    avatarStyle() {
      return common.getAvatarStyle(this.form)
    },
    userNameStyle() {
      return `/* Channel names */
yt-live-chat-text-message-renderer yt-live-chat-author-chip {
  margin-bottom: 5px;
}
yt-live-chat-text-message-renderer #content #author-name {
  ${this.form.randomUserNamesColor ? `color: var(--repeated-text-color) !important; ` : ''}
}
yt-live-chat-text-message-renderer #author-name[type="owner"],
yt-live-chat-text-message-renderer yt-live-chat-author-badge-renderer[type="owner"] {
  ${this.form.ownerUserNameColor ? `color: ${this.form.ownerUserNameColor} !important;` : ''}
}

yt-live-chat-text-message-renderer #author-name[type="moderator"],
yt-live-chat-text-message-renderer yt-live-chat-author-badge-renderer[type="moderator"] {
  ${this.form.moderatorUserNameColor ? `color: ${this.form.moderatorUserNameColor} !important;` : ''}
}

yt-live-chat-text-message-renderer #author-name[type="member"],
yt-live-chat-text-message-renderer yt-live-chat-author-badge-renderer[type="member"] {
  ${this.form.memberUserNameColor ? `color: ${this.form.memberUserNameColor} !important;` : ''}
}

yt-live-chat-text-message-renderer #author-name {
  ${this.form.showUserNames ? '' : 'display: none !important;'}
  ${this.form.userNameColor ? `color: ${this.form.userNameColor} !important;` : ''}
  font-family: "${common.cssEscapeStr(this.form.userNameFont)}"${common.FALLBACK_FONTS};
  font-size: ${this.form.userNameFontSize}px !important;
  line-height: ${this.form.userNameLineHeight || this.form.userNameFontSize}px !important;
}

/* Hide badges */
yt-live-chat-text-message-renderer #chat-badges {
  ${this.form.showBadges ? '' : 'display: none !important;'}
  vertical-align: text-top !important;
}
img.yt-live-chat-author-badge-renderer, yt-icon.yt-live-chat-author-badge-renderer {
  width: ${this.form.badgesSize}px;
  height: ${this.form.badgesSize}px;
}`
    },
    messageStyle() {
      return `/* Messages */
yt-live-chat-text-message-renderer #image-and-message,
yt-live-chat-text-message-renderer #image-and-message *,
yt-live-chat-text-message-renderer #message,
yt-live-chat-text-message-renderer #message * {
  ${this.form.messageColor ? `color: ${this.form.messageColor} !important;` : ''}
  font-family: "${common.cssEscapeStr(this.form.messageFont)}"${common.FALLBACK_FONTS};
  font-size: ${this.form.messageFontSize}px !important;
  line-height: ${this.form.messageLineHeight || this.form.messageFontSize}px !important;
}

yt-live-chat-text-message-renderer #image-and-message {
  display: block !important;
  overflow: visible !important;
  padding: 20px;
  border-radius: 14px;
}

yt-live-chat-text-message-renderer #message .emoji {
  width: auto !important;
  height: ${this.form.emoticonSize}px !important;
}

#image-and-message img[display="block"] {
  border-radius: ${this.form.emoticonBlockBorderRadius}px;
}

#image-and-message img[display="inline"] {
  border-radius: ${this.form.emoticonInlineBorderRadius}px;
}

${this.form.messageMergeSameUser ? `/* Thread 设定 */
#thread {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

#thread img.yt-img-shadow {
    visibility: hidden;
    height: 0;

}
#thread #card yt-live-chat-author-chip {
    display: none;
}
yt-live-chat-text-message-renderer #image-and-message {
  display: block !important;
  overflow: visible !important;
  margin-top:${this.form.messageGroupBlockPadding}px;
  padding: 14px;
  border-radius: 14px !important;
}
/* 单独处理圆角 */
yt-live-chat-text-message-renderer #thread>#card #image-and-message{
    border-top-left-radius: 4px !important;
    border-bottom-left-radius: 4px !important;
}
yt-live-chat-text-message-renderer #thread>#card:first-child #image-and-message{
    margin-top:4px;
    border-top-left-radius: 14px !important;
}
yt-live-chat-text-message-renderer #thread>#card:last-child #image-and-message{
    border-bottom-left-radius: 14px !important;
}
#thread>#card:first-child yt-live-chat-author-chip {
    display: flex;
}
#thread>#card:first-child img.yt-img-shadow {
    visibility: visible;
    height: auto;
}` : `/* The triangle beside dialog */
yt-live-chat-text-message-renderer #image-and-message::before {
  content: "";
  display: inline-block;
  position: absolute;
  top: ${this.form.showUserNames ? (this.form.userNameLineHeight || this.form.userNameFontSize) + 10 : 20}px;
  left: ${this.form.showAvatars ? this.form.avatarSize + (this.form.avatarSize / 4) - 8 : -8}px;
  border: 8px solid transparent;
  border-right: 18px solid;
  transform: rotate(35deg);
}`}

`
    },
    timeStyle() {
      return common.getTimeStyle(this.form)
    },
    backgroundStyle() {
      return `/* Background colors */
body {
  overflow: hidden;
  ${this.form.bgColor ? `background-color: ${this.form.bgColor};` : ''}
}

${this.getBgStyleForAuthorType('', this.form.messageBgColor)}

${this.getBgStyleForAuthorType('owner', this.form.ownerMessageBgColor)}

${this.getBgStyleForAuthorType('moderator', this.form.moderatorMessageBgColor)}

${this.getBgStyleForAuthorType('member', this.form.memberMessageBgColor)}`
    },
    scAndNewMemberStyle() {
      return `/* SuperChat/Fan Funding Messages */
yt-live-chat-paid-message-renderer {
  margin: 4px 0 !important;
}

${this.scAndNewMemberFontStyle}

yt-live-chat-membership-item-renderer #card,
yt-live-chat-membership-item-renderer #header {
  ${this.showNewMemberBgStyle}
}

${this.scTickerStyle}

${this.form.showOtherThings ? '' : `yt-live-chat-item-list-renderer {
  display: none !important;
}`}`
    },
    scAndNewMemberFontStyle() {
      return `yt-live-chat-paid-message-renderer #author-name,
yt-live-chat-paid-message-renderer #author-name *,
yt-live-chat-membership-item-renderer #header-content-inner-column,
yt-live-chat-membership-item-renderer #header-content-inner-column * {
  font-family: "${common.cssEscapeStr(this.form.firstLineFont)}"${common.FALLBACK_FONTS};
  font-size: ${this.form.firstLineFontSize}px !important;
  line-height: ${this.form.firstLineLineHeight || this.form.firstLineFontSize}px !important;
}

yt-live-chat-paid-message-renderer #purchase-amount,
yt-live-chat-paid-message-renderer #purchase-amount *,
yt-live-chat-membership-item-renderer #header-subtext,
yt-live-chat-membership-item-renderer #header-subtext * {
  font-family: "${common.cssEscapeStr(this.form.secondLineFont)}"${common.FALLBACK_FONTS};
  font-size: ${this.form.secondLineFontSize}px !important;
  line-height: ${this.form.secondLineLineHeight || this.form.secondLineFontSize}px !important;
}

yt-live-chat-paid-message-renderer #content,
yt-live-chat-paid-message-renderer #content * {
  font-family: "${common.cssEscapeStr(this.form.scContentFont)}"${common.FALLBACK_FONTS};
  font-size: ${this.form.scContentFontSize}px !important;
  line-height: ${this.form.scContentLineHeight || this.form.scContentFontSize}px !important;
}`
    },
    showNewMemberBgStyle() {
      return `background-color: ${this.form.memberUserNameColor} !important;
  margin: 4px 0 !important;`
    },
    scTickerStyle() {
      return `${this.form.showScTicker ? '' : `yt-live-chat-ticker-renderer {
  display: none !important;
}`}

/* SuperChat Ticker */
yt-live-chat-ticker-paid-message-item-renderer,
yt-live-chat-ticker-paid-message-item-renderer *,
yt-live-chat-ticker-sponsor-item-renderer,
yt-live-chat-ticker-sponsor-item-renderer * {
  font-family: "${common.cssEscapeStr(this.form.secondLineFont)}"${common.FALLBACK_FONTS};
}`
    },
    animationStyle() {
      return common.getAnimationStyle(this.form)
    }
  },
  watch: {
    result(val) {
      this.$emit('input', val)
      this.saveConfig()
    },
    filterText(val) {
      this.$refs.tree.filter(val)
    }
  },
  created() {
    this.$emit('input', this.result)
  },
  methods: {
    loadCSS(name) {
      if (hxcmLeak.list.has(name)) {
        this.$emit('input', hxcmLeak.list.get(name).css)
        this.saveConfig()
      }
    },
    filterNode(value, data) { return !value ? true : data.label.indexOf(value) !== -1 },
    saveConfig: _.debounce(() => {
      let config = mergeConfig(this.form, DEFAULT_CONFIG)
      window.localStorage.stylegenhxcmConfig = JSON.stringify(config)
    }, 500),
    loadConfig() {
      try {
        return mergeConfig(JSON.parse(window.localStorage.stylegenhxcmConfig), DEFAULT_CONFIG)
      } catch {
        return { ...DEFAULT_CONFIG }
      }
    },
    resetConfig() {
      this.form = { ...DEFAULT_CONFIG }
    },

    getBgStyleForAuthorType(authorType, color) {
      if (!color) {
        color = '#ffffff'
      }
      let typeSelector = authorType ? `[author-type="${authorType}"]` : ''
      return `yt-live-chat-text-message-renderer${typeSelector} #image-and-message {
  background-color: ${color} !important;
}

yt-live-chat-text-message-renderer${typeSelector} #image-and-message::before {
  border-right-color: ${color};
}`
    }
  }
}
</script>