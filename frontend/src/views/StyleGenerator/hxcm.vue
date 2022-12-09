<template>
  <div>
    <el-form label-width="150px" size="mini">
      <h3>样式选择</h3>
      <el-table id="hxcmlist" :data="styles" :default-sort="{ prop: 'updateTime', order: 'descending' }">
        <el-table-column prop="id" label="发布顺序" sortable width="100"> </el-table-column>
        <el-table-column prop="preview" label="预览" min-width="320">
          <template slot-scope="scope">
            <el-image :src="scope.row.preview" fit="contain"></el-image>
          </template>
        </el-table-column>
        <el-table-column prop="pid" label="商品ID" sortable width="88"> </el-table-column>
        <el-table-column prop="name" label="标题"> </el-table-column>
        <el-table-column prop="catalogue" label="类别" sortable width="100"> </el-table-column>
        <!-- <el-table-column prop="defaultWidth" label="建议宽度" sortable width="100"> </el-table-column> -->
        <el-table-column prop="updateTime" label="最后更新" sortable width="100"> </el-table-column>
        <el-table-column label="操作" width="88" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="getCSS(scope.row.id)">加载</el-button>
          </template>
        </el-table-column>
      </el-table>

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

#hxcmlist tr .id {
  width: 40px;
}

#hxcmlist tr .btn {
  width: 40px;
}
</style>

<script>
import { mergeConfig } from '@/utils'
import hxcmLeak from '@/loader'


export const DEFAULT_CONFIG = {
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
      styles: hxcmLeak.array()
    }
  },
  computed: {
    result() {
      return ``
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
    this.getCSS(24)
  },
  methods: {
    getCSS(id) {
      if (hxcmLeak.list.has(id)) {
        const URI = `static/pandamiao/style/${id}.css`
        const xhrFile = new XMLHttpRequest()
        const ts = this
        xhrFile.open("GET", URI, true)
        xhrFile.onload = () => {
          ts.$emit('input', xhrFile.response)
        }
        xhrFile.send()
      }
    },
    loadConfig() {
      try {
        return mergeConfig(JSON.parse(window.localStorage.stylegenhxcmConfig), DEFAULT_CONFIG)
      } catch {
        return { ...DEFAULT_CONFIG }
      }
    },
    resetConfig() {
      this.form = { ...DEFAULT_CONFIG }
    }
  }
}
</script>
