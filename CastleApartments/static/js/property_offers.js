const offerTableRows = document.getElementsByName("offer-table-row")
const propertyTableRows = document.getElementsByName("property-table-row")
let activeRow;

propertyTableRows.forEach((element) => {
    element.addEventListener("click", () => {
        visibleRows(element)
    })
})

const visibleRows = (element) => {
    if (activeRow) {
        activeRow.classList.toggle("table-active")
    }
    activeRow = element
    activeRow.classList.toggle("table-active")
    document.getElementById("offer-table").style.display = ""
    offerTableRows.forEach((el) => {
        document.getElementById("address-table-caller").innerHTML = element.id
        if (el.className === element.id) {
            el.style.display = ""
        } else {
        el.style.display = "none"
        }
    })
}


window.addEventListener("keydown", (event) => {
    if (["ArrowUp", "ArrowDown"].includes(event.key)) {
        let newRow;
        if (activeRow) {
            if (event.key == "ArrowUp") {
                newRow = activeRow.previousElementSibling ? activeRow.previousElementSibling : lastSibling()
                
            } else if (event.key == "ArrowDown") {
                newRow = activeRow.nextElementSibling ? activeRow.nextElementSibling : firstSibling()
            }
        } else {
            newRow = propertyTableRows[0]
        }
        visibleRows(newRow)
    }
})

const firstSibling = () => {
    const f = document.getElementById("seller-property-table-body").firstElementChild
    return f
}

const lastSibling = () => {
    const f = document.getElementById("seller-property-table-body").lastElementChild
    return f
}
