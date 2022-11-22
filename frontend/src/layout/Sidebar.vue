<template>
  <el-scrollbar wrap-class="scrollbar-wrapper">
    <el-menu
      router
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="rgb(64, 158, 255)"
      :default-active="$route.path"
    >
      <el-menu-item index="/">
        <i class="el-icon-s-home"></i>{{ $t('sidebar.home') }}
      </el-menu-item>
      <el-menu-item :index="$router.resolve({ name: 'stylegen' }).href">
        <i class="el-icon-brush"></i>样式选择器
      </el-menu-item>
      <a href="https://www.yuque.com/doodle-irifi/ueaigm/laogg2" target="_blank">
        <el-menu-item>
          <i class="el-icon-question"></i>{{ $t('sidebar.help') }}
        </el-menu-item>
      </a>
      <a href="https://github.com/DoodleBears/blivechat" target="_blank">
        <el-menu-item>
          <i class="el-icon-share"></i>只熊老师的项目地址
        </el-menu-item>
      </a>
      <a href="https://github.com/LaughsMan/blivechat_hxcmLeak" target="_blank">
        <el-menu-item>
          <i class="el-icon-share"></i>破解版的项目地址
        </el-menu-item>
      </a>
    </el-menu>
  </el-scrollbar>
</template>

<script>
import * as i18n from '@/i18n'

export default {
  name: 'Sidebar',
  data() {
    return {
      LOCALES: [
        { locale: 'zh', name: '中文' },
        { locale: 'ja', name: '日本語' },
        { locale: 'en', name: 'English' }
      ]
    }
  },
  methods: {
    onSelectLanguage(locale) {
      i18n.setLocale(locale)
    }
  }
}
</script>

<style>
.el-scrollbar {
  height: 100%;
}

.scrollbar-wrapper {
  overflow-x: hidden !important;
}

.scrollbar-wrapper .el-menu {
  border: none;
}
</style>
