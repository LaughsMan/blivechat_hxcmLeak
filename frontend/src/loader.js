import { hxcmData } from "./lastest"


class hxcmLeak {
    constructor() {
        console.log("Words that kill, would you speak them to me\nWith your breath so still, it makes me believe\nthe sins never die, can't wash this blood of our hands\nlet the world fear us all, it just means to an end\n\nour salvation lies, in the father's sins\nbeyond the truth, let me suffer now\nin my heart i just know that there's no way to light up the dark in his eyes")
        this.list = new Map()

        hxcmData.data.content.forEach(
            style => {
                let s = new hxcmStyle(style.id, style.pid, style.name, style.catalogue, style.coverImage, style.defaultWidth, style.updateTime)
                this.list.set(s.id, s)
            })
        console.log(`共加载了${this.list.size}个样式`)
    }

    list = null

    array() {
        return Array.from(this.list.values((a, b) => { return a.updateTime.localeCompare(b.updateTime) }))
    }
}

class hxcmStyle {
    constructor(id, pid, name, catalogue, preview, defaultWidth, updateTime) {
        this.id = id
        this.pid = pid
        this.name = name
        this.catalogue = catalogue
        this.defaultWidth = defaultWidth
        this.preview = preview
        this.updateTime = updateTime
    }

}

export default new hxcmLeak()

