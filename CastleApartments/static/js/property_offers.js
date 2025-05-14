
// property-line to offer-table
(() => {
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
            try {
                notifications = element.getElementsByClassName("notification-pill")
                notifications.forEach((notification) => {
                    notification.remove()
                })
            } catch (err) {}
        }
        activeRow = element
        activeRow.classList.toggle("table-active")
        let imageElement = document.getElementById("chosen-row-property-image")
        imageElement.src = element.getAttribute("data-image")
        //imageElement.parentElement.setAttribute("href", `/real-estates/${element.getAttribute("data-id")}`)
        imageElement.parentElement.innerHTML = element.getAttribute("data-card")
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
        return document.getElementById("seller-property-table-body").firstElementChild
    }
    
    const lastSibling = () => {
        return document.getElementById("seller-property-table-body").lastElementChild
    }

})();


//resets the edit property modal when its closed


let form = Array.from(document.forms).filter((f) => f.id === "create-new-property")[0]
const submittedImageRow = document.getElementById("added-images-row-submit")
const imageRow = document.getElementById("new-images-row")
const imgDesc = document.getElementById("new-image-description") 
let imageObjs = []
let imageElements = []
const imgInput = document.getElementById("new-image-file-input")
const submitButtons = document.getElementsByName("add-all-images-button") // classname ("image-modal-submit-btn")
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
});

const imgAdderButton = document.getElementById("image-adder-button")
imgAdderButton.addEventListener("click", () => {
    const file = imgInput.files[0]
    if (!file) {
        imgInput.setAttribute("isvalid", "true")
    } else {
        imgInput.setAttribute("isvalid", "false")
    }
    if (!imgDesc.value) {
        imgDesc.setAttribute("isvalid", "true")
    } else {
        imgDesc.setAttribute("isvalid", "false")
    }
    if (file && imgDesc.value) {
        let desc = imgDesc.value
        let imgElement = newImageElement(file, desc)
        imageRow.appendChild(imgElement)
        imgDesc.value = ""
        imgInput.value = ""

    }
});

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
};


const createPropertyButton = document.getElementById("create-property-button")
const editPropertyButtons = document.getElementsByName("editProperty")
const propertySubmitButton = document.getElementById("create-property-modal-submit");
const extrasField = [...document.querySelectorAll('[id^="extra-option-"]')]



document.addEventListener("DOMContentLoaded", () => {
    const modal = document.querySelector('[id="property-modal"]');
    modal.addEventListener("hidden.bs.modal", () => {
        clearFormImages();
    });
});

createPropertyButton.addEventListener("click", () => {
    propertySubmitButton.disabled = true
    document.getElementById("create-property-modal").innerHTML = "Skrá eign"
    form.action = "/real-estates/"
    setFormValue("streetname", "")
    setFormValue("city_input", "")
    setFormValue("zip", "")
    setFormValue("price", "")
    setFormValue("type", "")
    setFormValue("bedrooms", "")
    setFormValue("bathrooms", "")
    setFormValue("sqm", "")
    setFormValue("desc", "")
    extrasField.forEach((field) => {
        field.removeAttribute("checked")
    })
    clearFormImages()
});

const clearFormImages = () => {
    let images = form.querySelector('input[name="hidden-images-list"]')
    images.setAttribute("value", "")
    submittedImageRow.innerHTML = ""
};


Array.from(editPropertyButtons).forEach((element) => {
    element.addEventListener("click", () => {

        propertySubmitButton.disabled = false
        document.getElementById("create-property-modal").innerHTML = "Breyta eign"
        setFormValue("streetname", element.getAttribute("data-street"))
        setFormValue("city_input", element.getAttribute("data-city"))
        setFormValue("zip", element.getAttribute("data-zip"))
        setFormValue("price", element.getAttribute("data-price"))
        setFormValue("type", element.getAttribute("data-type"))
        setFormValue("bedrooms", element.getAttribute("data-bedrooms"))
        setFormValue("bathrooms", element.getAttribute("data-bathrooms"))
        setFormValue("sqm", element.getAttribute("data-sqm"))
        setFormValue("desc", element.getAttribute("data-desc"))
        form["desc"].innerHTML = element.getAttribute("data-desc")
        form["desc"].value = element.getAttribute("data-desc")
        let extras = element.getAttribute("data-extras").split(",")
        extrasField.forEach((field) => {
            if (extras.includes(field.value)) {
                field.checked = true
            } else {
                field.checked = false
            }
        })

        const listener = () => {
        
            let street = element.getAttribute("data-street")
            let zip = element.getAttribute("data-zip")
            let city = element.getAttribute("data-city")
            let rowId = `${street} - ${zip} ${city}`
            clearFormImages()
            editPropertyOnSubmit(element.getAttribute("data-id"), rowId)
            propertySubmitButton.removeEventListener("click", listener)
        }
        propertySubmitButton.addEventListener("click", listener)
    })
});


const editPropertyOnSubmit = (id, rowId) => {
    let editForm = $("#create-new-property")
    $("#create-new-property").submit( function (e) {
        e.preventDefault()

        let rowElement = document.getElementById(rowId)
        changeRow(rowElement, editForm)
        document.getElementById("offer-table").style.display = "none"
        document.getElementById("address-table-caller").innerHTML = ""
        })

        newExtras = extrasField.map((field) => {
            console.log(field.value)
                if (field.checked) {
            console.log(field.value)
                    return field.value
                }
            })
        console.log(newExtras)
        let data = editForm.serializeArray()
        data.push({name: "action", value: "PATCH"})
        data.push({name: "extras", value: newExtras})

        $.ajax({
            type: "POST",
            url: `/real-estates/${id}`,
            data: 
                data
            ,

        })
};

const changeRow = (element, information) => {
    
    let aCell = element.querySelector('th[name="address-cell"]')
    let pCell = element.querySelector('td[name="price-cell"]')
    information = information[0]
    
    let street = information.querySelector('input[id="property-input-streetname"]').value
    let city = information.querySelector('input[id="property-input-city-input"]').value
    let price = information.querySelector('input[id="property-input-price"]').value
    let zip = information.querySelector('input[id="property-input-zip"]').value
    let bedrooms = information.querySelector('input[id="property-input-bedrooms"]').value
    let bathrooms = information.querySelector('input[id="property-input-bathrooms"]').value
    let sqm = information.querySelector('input[id="property-input-sqm"]').value
    let type = information.querySelector('select[id="property-input-type"]').value
    let desc = information.querySelector('textarea[id="property-input-desc"]').value
    let address = `${street} - ${zip} ${city}`

    element.setAttribute("data-streetname", street)
    element.setAttribute("data-price", price)
    element.setAttribute("data-city_input", city)
    element.setAttribute("data-zip", zip)
    element.setAttribute("data-desc", desc)
    element.setAttribute("data-bedrooms", bedrooms)
    element.setAttribute("data-bathrooms", bathrooms)
    element.setAttribute("data-sqm", sqm)
    element.setAttribute("data-type", type)
    
    
    aCell.innerHTML = `<h4 class="mx-5">${address}</h4>`
    pCell.innerHTML = `<h4>${parseInt(price).toLocaleString().replace(/,/g,".")} kr.</h4>`
};

const setFormValue = (formfield, val) => {
        form[formfield].setAttribute("value", val)
        form[formfield].value = val
};

(() => {
    const deletePropertyButtons = document.getElementsByName("deleteProperty")
    
    deletePropertyButtons.forEach((element) => {
        
        const listener = () => {
            document.getElementById("delete-property-modal-body-prompt").innerHTML = `Ertu viss um að þú viljir eyða ${element.getAttribute("data-street")}?`
            let street = element.getAttribute("data-street")
            let zip = element.getAttribute("data-zip")
            let city = element.getAttribute("data-city")
            let rowId = `${street} - ${zip} ${city}`
    
            deletePropertyOnSubmit(element.getAttribute("data-id"), rowId)
            element.removeEventListener("click", listener)
        }
        element.addEventListener("click", listener)
    })
    
    const deletePropertyOnSubmit = (id, rowId) => {
        $("#delete-property-form").submit( function (e) {
            e.preventDefault()
    
            let rowElement = document.getElementById(rowId)
            rowElement.remove()
    
            $.ajax({
                type: "POST",
                url: `/real-estates/${id}`,
                data: {
                    action: "DELETE",
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
                },
    
            })
        })
    }
})();


// Accept offer 
(() => {
    const accepterTextDiv = (element) => {
        div = document.getElementById("accept-offer-modal-body-prompt")
        let price = element.getAttribute("data-offer-amount")
        let street = element.getAttribute("data-street")
        let zip = element.getAttribute("data-zip")
        let city = element.getAttribute("data-city")
        let address = `${street} - ${zip} ${city}`
        
        let breaker = document.createElement("br")
        let top = document.createElement("h4")
        top.innerHTML = "Þú ert hér með að samþykkja sölu á "
        top.classList.add("text-break")

        let inner = document.createElement("h3")
        inner.classList.add("text-center")
        inner.classList.add("fw-semibold")
        inner.classList.add("lh-lg")
        inner.classList.add("text-decoration-underline")

        inner.innerHTML = address

        let bottom = document.createElement("h4")
        bottom.classList.add("text-end")
        bottom.classList.add("px-2")
        bottom.innerHTML = `fyrir <u>${price}</u> kr.`

        div.innerHTML = ""
        div.appendChild(top)
        div.appendChild(breaker)
        div.appendChild(inner)
        div.appendChild(breaker)
        div.appendChild(bottom)
    }
    
    const acceptOfferButtons = document.getElementsByName("accept-offer-button")
    let acceptSubmitButton = document.getElementById("accept-offer-submit-button")
    
    acceptOfferButtons.forEach((element) => {
        
        const listener = () => {
            div = document.getElementById("accept-offer-modal-body-prompt")
            let price = element.getAttribute("data-offer-amount")
            let street = element.getAttribute("data-street")
            let zip = element.getAttribute("data-zip")
            let city = element.getAttribute("data-city")
            let address = `${street} - ${zip} ${city}`
            
            let breaker = document.createElement("br")
            let top = document.createElement("h4")
            top.innerHTML = "Þú ert hér með að samþykkja sölu á "
            top.classList.add("text-break")
        
            let inner = document.createElement("h3")
            inner.classList.add("text-center")
            inner.classList.add("fw-semibold")
            inner.classList.add("lh-lg")
            inner.classList.add("text-decoration-underline")
        
            inner.innerHTML = address
        
            let bottom = document.createElement("h4")
            bottom.classList.add("text-end")
            bottom.classList.add("px-2")
            bottom.innerHTML = `fyrir <u>${price}</u> kr.`
        
            div.innerHTML = ""
            div.appendChild(top)
            div.appendChild(breaker)
            div.appendChild(inner)
            div.appendChild(breaker)
            div.appendChild(bottom)
            id = element.getAttribute("data-id")
            rowId = `offer-id-${id}-row`
            accepterTextDiv(element)


            acceptSubmitButton.addEventListener("click", () => {
                acceptOfferRow(element)
                acceptOfferOnSubmit(id)
                })
            element.removeEventListener("click", listener)
            }
                
        element.addEventListener("click", listener)
    })


    const acceptOfferOnSubmit = (id) => {
        $("#accept-offer-form").submit( (e) => {
            
            e.preventDefault()
            
            $.ajax({
                type: "POST",
                url: `/offers/${id}`,
                data: {
                    action: "ACCEPT",
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
                },
            })
        })
    }

// Reject offer
    const rejectOfferButtons = document.getElementsByName("reject-offer-button")
    let rejectSubmitButton = document.getElementById("reject-offer-submit-button")

    rejectOfferButtons.forEach((element) => {
        
        const listener = () => {
            let price = element.getAttribute("data-offer-amount")
            document.getElementById("reject-offer-modal-body-prompt").innerHTML = `Ertu viss um að þú viljir hafna þessu einstaka tækifæri til að græða ${price} kr.?`
    
            id = element.getAttribute("data-id")
            rowId = `offer-id-${id}-row`
    
            rejectSubmitButton.addEventListener("click", () => {
                rejectOfferOnSubmit(id, rowId)
                element.removeEventListener("click", listener)
            })
        }
        element.addEventListener("click", listener)
    })


    const rejectOfferOnSubmit = (id, rowId) => {
        $("#reject-offer-form").submit( (e) => {
            console.log("rejecting offer")
            e.preventDefault()
            let rowElement = document.getElementById(rowId)
            rowElement.remove()
            $.ajax({
                type: "POST",
                url: `/offers/${id}`,
                data: {
                    action: "REJECT",
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
                },
            })
        })
    }


// Delete offer

    const deleteOfferButtons = document.getElementsByName("delete-offer-button")
    let deleteSubmitButton = document.getElementById("delete-offer-submit-button")

    deleteOfferButtons.forEach((element) => {
        const listener = () => {
            document.getElementById("delete-offer-modal-body-prompt").innerHTML = `Þangað til næst! ;`
    
                id = element.getAttribute("data-id")
                rowId = `offer-id-${id}-row`
    
                deleteSubmitButton.addEventListener("click", () => {
                    deleteOfferOnSubmit(id, rowId)
                })
                element.removeEventListener("click", listener)
        }
            element.addEventListener("click", listener)
    })


    const deleteOfferOnSubmit = (id, rowId) => {
        $("#delete-offer-form").submit( (e) => {
            
            e.preventDefault()
            let rowElement = document.getElementById(rowId)
            rowElement.remove()
            $.ajax({
                type: "POST",
                url: `/offers/${id}`,
                data: {
                    action: "DELETE",
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
                },
            })
        })
    }


// Contingent offer
    
    const contingentOfferButtons = document.getElementsByName("contingent-offer-button")
    let contingentSubmitButton = document.getElementById("contingent-offer-submit-button")

    contingentOfferButtons.forEach((element) => {
        
        const listener = () => {
            let div = document.createElement("div")
            div.classList.add("form-floating")
            let text = document.createElement("textarea")
            text.setAttribute("id", "id_bio")
            text.setAttribute("name", "bio")
            text.classList.add("form-control")
            text.style.height = "8rem"
            let label = document.createElement("label")
            label.setAttribute("for", "id_bio")
            div.appendChild(text)
            div.appendChild(label)

            document.getElementById("contingent-offer-modal-body-prompt").innerHTML = ""
            document.getElementById("contingent-offer-modal-body-prompt").appendChild(div)
            id = element.getAttribute("data-id")

            contingentSubmitButton.addEventListener("click", () => {
                acceptOfferRow(element)
                contingentOfferOnSubmit(id, text)
            })
        element.removeEventListener("click", listener)
        }    
    element.addEventListener("click", listener)
    })

    const contingentOfferOnSubmit = (id, textarea) => {
        $("#contingent-offer-form").submit( (e) => {
            
            e.preventDefault()
            e.stopPropagation()
            
            $.ajax({
                type: "POST",
                url: `/offers/${id}`,
                data: {
                    action: "CONTINGENT",
                    message: textarea.value,
                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
                },
            })
        })
        //$("#contingent-offer-form")[0].reset()

    }

    const propertyFields = document.querySelectorAll('[id^="property-input"]');
    const propertySubmitButton = document.getElementById("create-property-modal-submit");
    
    propertyFields.forEach((element) => {
        element.addEventListener("change", () => {
            
            if (Array.from(propertyFields).map((el) => el.checkValidity()).reduce((f, s) => f && s)) {
                propertySubmitButton.disabled = false;
            } else {
                propertySubmitButton.disabled = true;
            }
    
            if (!element.checkValidity()) {
                element.setAttribute("isvalid", "true");
                element.parentElement.querySelector(".invalid-text").style.display = "block"; 
            } else {
                element.removeAttribute("isvalid");
                element.parentElement.querySelector(".invalid-text").style.display = "none"; 
            }
        });
    
    
        
        });
    
    const disableOfferRow = (element, row) => {
        let buttons = row.getElementsByTagName("button")
        Array.from(buttons).forEach((button) => {
            if (!(button.parentElement == element.parentElement) || button.innerHTML != "Samþykkja" || element.innerHTML == "Samþykkja") {
                button.setAttribute("disabled", true)
                button.innerHTML = ""
            }
        })
    }

    const acceptOfferRow = (element) => {
        address = document.getElementById("address-table-caller").innerHTML
        propRow = document.getElementById(address)
        console.log(propRow)
        allRows = document.getElementsByClassName(address)
        propRow.getElementsByClassName("status-cell")[0].innerHTML = "<h4><b>SOLD</b></h4></td>"
        let propButtons = propRow.getElementsByTagName("button")
        Array.from(propButtons).forEach((button) => {
            button.innerHTML = ""
            button.setAttribute("disabled", true)
        })
        Array.from(allRows).forEach((row) => disableOfferRow(element, row))
    }

})();