import { hxcmData } from "./lastest"


class hxcmLeak {
    constructor() {
        console.log("不用查了，淘宝奸商，你妈死了，人在脚盆，欢迎报警，开源万岁")
        this.list = new Map()

        hxcmData.data.content.forEach(
            style => {
                let s = new hxcmStyle(style.materialName, style.catalogue, `https://hxcm.pandamiao.com/bullet-chat/image/${style.coverImage}`, style.content)
                this.list.set(s.name, s)
            })
        console.log(this.list)
        console.log(`共加载了${this.list.size}个样式`)
    }

    list = null

    array() {
        return Array.from(this.list.values()).sort(
            (a, b) => {
                return a.name.localeCompare(b.name)
            })
    }

    get_Name(id) {
        return this.list.has(id) ? hxcmLeak.list.get(id).name : "无效ID"
    }

    get_CSS(id) {
        return this.list.has(id) ? hxcmLeak.list.get(id).css : "无效ID"
    }

    cssinput = null
}

class hxcmStyle {
    constructor(name, catalogue, preview, css) {
        this.name = name
        this.catalogue = catalogue
        this.preview = preview
        this.css = css
    }

    load() {

    }
}

export default new hxcmLeak()

