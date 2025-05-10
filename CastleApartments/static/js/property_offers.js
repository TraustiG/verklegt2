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
        event.preventDefault()
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


//resets the edit property modal when its closed
document.addEventListener("DOMContentLoaded", () => {
    const modals = document.querySelectorAll('[id^="edit-property-modal-"]');

    modals.forEach((modalEl) => {
        modalEl.addEventListener("hidden.bs.modal", () => {
            modalEl.querySelector("form").reset();
        });
    });
});


const submitButtons = document.getElementsByName("add-all-images-button") // classname ("image-modal-submit-btn")
const imageReader = new FileReader();
const imgAdderButton = document.getElementById("image-adder-button")
const imgInput = document.getElementById("new-image-file-input")
const imgDesc = document.getElementById("new-image-description") 
const imageRow = document.getElementById("new-images-row")
const submittedImageRow = document.getElementById("added-images-row-submit")
const editPropertyButtons = document.getElementsByName("editProperty")
const createPropertyButton = document.getElementById("makeOffer")
let form = Array.from(document.forms).filter((f) => f.id === "create-new-property")[0]
let imageObjs = []
let imageElements = []


submitButtons.forEach((el) => {
    el.addEventListener("click", () => {
        if (el.classList.contains("image-modal-submit-btn")) {
            let images = form.querySelector('input[name="hidden-images-list"]')
            if (images.getAttribute("value")) {
                let oldImages = JSON.parse(images.getAttribute("value"))
                imageObjs = oldImages.concat(imageObjs)
            }
            imageElements.forEach((imgEl) => {
                submittedImageRow.appendChild(imgEl)
            })
            images.setAttribute("value", JSON.stringify(imageObjs))
        }
    
        imageObjs = []
        imageRow.innerHTML = ""
        imgDesc.value = ""
        imgInput.value = ""
    })
})


imgAdderButton.addEventListener("click", () => {
    const file = imgInput.files[0]
    if (file && imgDesc.value) {
        let desc = imgDesc.value
        let imgElement = newImageElement(file, desc)
        imageRow.appendChild(imgElement)
        imgDesc.value = ""
        imgInput.value = ""

    } else {
        console.log("input??")
    }
})


const newImageElement = (file, desc) => {

    let div = document.createElement("div")
    div.classList.add("align-self-end")
    div.classList.add("col-2")
    div.classList.add("d-flex")
    div.classList.add("justify-content-center")

    let row = document.createElement("div")
    row.classList.add("row")
    row.classList.add("image-thumbnail")

    let img = document.createElement("img")
    let reader = new FileReader()
    reader.onload = () => {
        img.src = reader.result
        imageObjs.push({url: reader.result, desc: desc})
    }
    reader.readAsDataURL(file)
    img.style.position = "relative"
    
    let name = document.createElement("label")
    name.classList.add("text-center")
    name.classList.add("text-truncate")
    name.innerHTML = desc

    row.appendChild(img)
    row.appendChild(name)
    div.appendChild(row)
    imageElements.push(div)

    return div
}

/*
reyna eyða myndum ??

const xSvg = "<svg fill='#e10000' height='64px' width='64px' version='1.1' id='Capa_1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 415.188 415.188' xml:space='preserve' stroke='#e10000'><g id='SVGRepo_bgCarrier' stroke-width='0'></g><g id='SVGRepo_tracerCarrier' stroke-linecap='round' stroke-linejoin='round'></g><g id='SVGRepo_iconCarrier'> <path d='M412.861,78.976c3.404-6.636,2.831-14.159-0.15-20.404c0.84-7.106-1.02-14.321-7.746-19.855 c-6.262-5.151-12.523-10.305-18.781-15.457c-11.005-9.055-28.237-11.913-38.941,0c-48.619,54.103-99.461,105.856-152.167,155.725 c-39.185-36.605-78.846-72.713-118.223-108.868c-13.82-12.693-33.824-8.71-42.519,6.411c-12.665,6.286-22.931,14.481-31.42,28.468 c-4.042,6.664-3.727,15.076,0,21.764c25.421,45.578,74.557,85.651,114.957,122.529c-5.406,4.839-10.772,9.724-16.287,14.461 c-54.43,46.742-91.144,76.399-23.029,124.325c0.919,0.647,1.856,0.504,2.789,0.882c1.305,0.602,2.557,1.026,4.004,1.264 c0.45,0.017,0.87,0.093,1.313,0.058c1.402,0.114,2.774,0.471,4.195,0.192c36.621-7.18,70.677-35.878,101.576-67.48 c30.1,29.669,62.151,58.013,97.395,74.831c8.391,4.005,18.395,1.671,24.855-3.931c10.832,0.818,20.708-5.913,25.665-15.586 c0.734-0.454,1.207-0.713,2.002-1.21c15.748-9.838,17.187-29.431,5.534-42.936c-26.313-30.492-54.284-59.478-82.798-87.95 C316.426,196.043,380.533,141.939,412.861,78.976z'></path> </g></svg>"
const createRedCross = () => {
    let div = document.createElement("div")
    div.style.position = "absolute"
    let x = document.createElement("span")
    x.innerHTML = xSvg
    x.style.visibility = "hidden"
    x.style.position = "absolute"
    div.appendChild(x)
    return div
}
*/

editPropertyButtons.forEach((element) => {
    element.addEventListener("click", () => {
        document.getElementById("create-property-modal").innerHTML = "Breyta eign"
        form.action = `/edit-property/${element.getAttribute("data-id")}/`
        
        form["streetname"].setAttribute("value", element.getAttribute("data-street"))
        form["city_input"].setAttribute("value", element.getAttribute("data-city"))
        form["zip"].setAttribute("value", element.getAttribute("data-zip"))
        form["price"].setAttribute("value", element.getAttribute("data-price"))
        form["type"].setAttribute("value", element.getAttribute("data-type"))
        form["bedrooms"].setAttribute("value", element.getAttribute("data-bedrooms"))
        form["bathrooms"].setAttribute("value", element.getAttribute("data-bathrooms"))
        form["sqm"].setAttribute("value", element.getAttribute("data-sqm"))
        form["desc"].innerHTML = element.getAttribute("data-desc")
    })
})

createPropertyButton.addEventListener("click", () => {
    document.getElementById("create-property-modal").innerHTML = "Skrá eign"
    form.action = "/create-property"
    
    form["streetname"].setAttribute("value", "")
    form["city_input"].setAttribute("value", "")
    form["zip"].setAttribute("value", "")
    form["price"].setAttribute("value", "")
    form["type"].setAttribute("value", "")
    form["bedrooms"].setAttribute("value", "")
    form["bathrooms"].setAttribute("value", "")
    form["sqm"].setAttribute("value", "")
    form["desc"].innerHTML = ""
})