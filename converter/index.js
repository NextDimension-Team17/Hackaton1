const csv = require('csv-parser')
const fs = require('fs')

const sourceName = 'data/wiki.csv'
const destinationName = 'data/converted.json'
const destinationJs = 'data/converted.js'


const parent = {
    name: '',
    url: 'None',
    children: []
}
let r = null

fs.createReadStream(sourceName)
    .pipe(csv())
    .on('data', (row) => {
        r = row
        putNode(parent)
    })
    .on('end', () => {
        const stringify = JSON.stringify(parent, null, 4)
        const unquoted = stringify.replace(/"([^"]+)":/g, '$1:');

        fs.writeFileSync(destinationName, stringify)
        fs.writeFileSync(destinationJs, `const json = ${unquoted}`)
    })

const putNode = (elem) => {
    if (r.parent_url === elem.url) {
        elem.children.push(createNode(r))
        return
    }

    elem.children.forEach((node) => putNode(node))
}

const createNode = (row) => {
    const { title, url } = row

    return {
        name: title,
        url,
        children: []
    }
}
