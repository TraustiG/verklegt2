const tables = document.getElementsByTagName("table")

Array.from(tables).forEach((table) => {
    let head = table.getElementsByTagName("thead")[0]
    let headers = head.getElementsByTagName("th")
    Array.from(headers).forEach((header, i) => {
        if (header.innerHTML != "") {
            let sortType = header.getAttribute("name")
            header.addEventListener("click", () => sortTable(table, i, sortType))
        }
    })
})


const sortTable = (table, n, sortType) => {
    var rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0
    switching = true
    dir = "asc"
    let counter = 1
    while (switching) {
        switching = false
        rows = table.rows
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false
            x = rows[i].getElementsByClassName("table-cell-sorter")[n].innerHTML
            y = rows[i + 1].getElementsByClassName("table-cell-sorter")[n].innerHTML
            if (sortType === "date") {
                x = new Date(Date.parse(x))
                y = new Date(Date.parse(y))
            } else if (sortType === "numeric") {
            
                x = parseInt(x.replace(/.*?>([\d\.]*).*/g, "$1").replace(/\./g, ""))
                y = parseInt(y.replace(/.*?>([\d\.]*).*/g, "$1").replace(/\./g, ""))
            } else {
                x = x.toLowerCase()
                y = y.toLowerCase()
            }
            counter = 2
            if (dir == "asc") {
                if (x > y) {
                shouldSwitch = true
                break
                }
            } else {
                if (x < y) {
                shouldSwitch = true
                break
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i])
            switching = true
            switchcount ++
        } else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc"
                switching = true
            }
        }
    }
}