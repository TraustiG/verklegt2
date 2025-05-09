const offerTableRows = document.getElementsByName("offer-table-row")
const propertyTableRows = document.getElementsByName("property-table-row")
let activeRow;
console.log(activeRow)

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
    console.log(activeRow)
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
                console.log(newRow)
                
            } else if (event.key == "ArrowDown") {
                newRow = activeRow.nextElementSibling ? activeRow.nextElementSibling : firstSibling()
                console.log(newRow)
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


//resets the edit property modal when its closed
document.addEventListener("DOMContentLoaded", () => {
    const modals = document.querySelectorAll('[id^="edit-property-modal-"]');

    modals.forEach((modalEl) => {
        modalEl.addEventListener("hidden.bs.modal", () => {
            modalEl.querySelector("form").reset();
        });
    });
});