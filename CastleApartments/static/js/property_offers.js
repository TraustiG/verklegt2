

// property-line to offer-table
(() => {
    const offerTableRows = document.getElementsByName("offer-table-row")
    const propertyTableRows = document.getElementsByName("property-table-row")
    const deletePropertySoloButton = document.querySelector('[id="delete-property-single-button"]')
    const editPropertySoloButton = document.querySelector('[id="edit-property-single-button"]')
    const createPropertyButton = document.getElementById("create-property-button")
    const deletePropertyButton = document.getElementById("delete-property-submit-button")
    const propertySubmitButton = document.getElementById("create-property-modal-submit");
    const extrasField = [...document.querySelectorAll('[id^="extra-option-"]')]
    const imageElement = document.getElementById("chosen-row-property-image")
    const addressLine = document.getElementById("address-table-caller")
    let activeRow;
    
    propertyTableRows.forEach((element) => {
        element.addEventListener("click", () => {
            visibleRows(element)
        })
    });
    
    const visibleRows = (element) => {
        if (activeRow) {
            activeRow.classList.toggle("table-active")
            try {
                notifications = element.getElementsByClassName("notification-pill")
                notifications.forEach((notification) => {
                    notification.remove()
                })
            } catch (err) {}
        } else {
            deletePropertySoloButton.style.display = ""
            editPropertySoloButton.style.display = ""
        }

        let status = element.getAttribute("data-status")
        if (["PROCESSED", "SOLD"].includes(status)) {
            editPropertySoloButton.innerHTML = ""
            editPropertySoloButton.disabled = true
            if (status === "SOLD") {
                deletePropertySoloButton.innerHTML = ""
                deletePropertySoloButton.disabled = true
            }
        } else {
            editPropertySoloButton.innerHTML = "Breyta"
            editPropertySoloButton.disabled = false
            deletePropertySoloButton.innerHTML = "Eyða"
            deletePropertySoloButton.disabled = false
        }
            

        activeRow = element
        addressLine.innerHTML =  `${element.getAttribute("data-street")} - ${element.getAttribute("data-zip")} ${element.getAttribute("data-city")}`
        activeRow.classList.toggle("table-active")
        imageElement.src = element.getAttribute("data-image")
        imageElement.parentElement.setAttribute("href", `/real-estates/${element.getAttribute("data-id")}`)
        document.getElementById("offer-table").style.display = ""
        offerTableRows.forEach((el) => {
            if (el.className === element.getAttribute("data-address")) {
                el.style.display = ""
            } else {
            el.style.display = "none"
            }
        })
    }

    const clearView = () => {
        deletePropertySoloButton.style.display = "none"
        editPropertySoloButton.style.display = "none"
        addressLine.innerHTML = ""
        imageElement.src = ""
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
    });

    const firstSibling = () => {
        return document.getElementById("seller-property-table-body").firstElementChild
    }
    
    const lastSibling = () => {
        return document.getElementById("seller-property-table-body").lastElementChild
    }
    
    editPropertySoloButton.addEventListener("click", () => {

        propertySubmitButton.disabled = false
        document.getElementById("create-property-modal").innerHTML = "Breyta eign"

        const activeRow = document.querySelector('tr[class="table-active"]')
        setFormValue("streetname", activeRow.getAttribute("data-street"))
        setFormValue("city_input", activeRow.getAttribute("data-city"))
        setFormValue("zip", activeRow.getAttribute("data-zip"))
        setFormValue("price", activeRow.getAttribute("data-price"))
        setFormValue("type", activeRow.getAttribute("data-type"))
        setFormValue("bedrooms", activeRow.getAttribute("data-bedrooms"))
        setFormValue("bathrooms", activeRow.getAttribute("data-bathrooms"))
        setFormValue("sqm", activeRow.getAttribute("data-sqm"))
        setFormValue("desc", activeRow.getAttribute("data-desc"))
        form["desc"].innerHTML = activeRow.getAttribute("data-desc")
        form["desc"].value = activeRow.getAttribute("data-desc")
        let extras = activeRow.getAttribute("data-extras").split(",")
        extrasField.forEach((field) => {
            if (extras.includes(field.value)) {
                field.checked = true
            } else {
                field.checked = false
            }
        })

        const listener = () => {
        
            clearFormImages()
            editPropertyOnSubmit(activeRow.getAttribute("data-id"), activeRow.id)
            propertySubmitButton.removeEventListener("click", listener)
        }
        propertySubmitButton.addEventListener("click", listener)
    });


    const editPropertyOnSubmit = (id, rowId) => {
        let editForm = $("#create-new-property")

        $("#create-new-property").submit( function (e) {
            e.preventDefault()

            let rowElement = document.getElementById(rowId)
            changeRow(rowElement, editForm)
            document.getElementById("offer-table").style.display = "none"
            addressLine.innerHTML = ""
            newExtras = extrasField.map((field) => {
                if (field.checked) {
                    return field.value
                }
            })
                
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
            editForm.unbind()
        })
    };

    const changeRow = (element, information) => {
        
        information = information[0]
        let street = information.querySelector('input[id="property-input-streetname"]').value
        let city = information.querySelector('input[id="property-input-city-input"]').value
        let zip = information.querySelector('input[id="property-input-zip"]').value
        
        let aCell = activeRow.querySelector('th[name="address-cell"]')
        let pCell = activeRow.querySelector('td[name="price-cell"]')
        
        let price = information.querySelector('input[id="property-input-price"]').value
        let bedrooms = information.querySelector('input[id="property-input-bedrooms"]').value
        let bathrooms = information.querySelector('input[id="property-input-bathrooms"]').value
        let sqm = information.querySelector('input[id="property-input-sqm"]').value
        let type = information.querySelector('select[id="property-input-type"]').value
        let desc = information.querySelector('textarea[id="property-input-desc"]').value
        activeRow.setAttribute("data-street", street)
        activeRow.setAttribute("data-price", price)
        activeRow.setAttribute("data-city", city)
        activeRow.setAttribute("data-zip", zip)
        activeRow.setAttribute("data-desc", desc)
        activeRow.setAttribute("data-bedrooms", bedrooms)
        activeRow.setAttribute("data-bathrooms", bathrooms)
        activeRow.setAttribute("data-sqm", sqm)
        activeRow.setAttribute("data-type", type)
        
        aCell.innerHTML = `<h5 class="mx-5">${street}</h5><h5>${zip} ${city}</h5>`
        pCell.innerHTML = `<h5>${parseInt(price).toLocaleString().replace(/,/g,".")} kr.</h5>`
    };

    const setFormValue = (formfield, val) => {
            form[formfield].setAttribute("value", val)
            form[formfield].value = val
    };
    
    deletePropertySoloButton.addEventListener("click", (e) => {
        
        let deletePrompt = document.querySelector('[id="delete-property-modal-body-prompt"]')
        deletePrompt.innerHTML = `Ertu viss um að þú viljir eyða ${activeRow.getAttribute("data-street")}?`
        
        const listener = () => {
            clearView()
            let id = activeRow.getAttribute("data-id")
            deletePropertyOnSubmit(id, activeRow.id)
            deletePropertyButton.removeEventListener("click", listener)
        }
        deletePropertyButton.addEventListener("click", listener)
    });

    
    const deletePropertyOnSubmit = (id, rowId) => {
        const editForm = $("#delete-property-form")

        editForm.submit( function (e) {
            e.preventDefault()
            e.stopPropagation()
    
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
            editForm.unbind()
        })
    }

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
            field.checked = false
        })
        clearFormImages()
    });

    const clearFormImages = () => {
        let images = form.querySelector('input[name="hidden-images-list"]')
        images.setAttribute("value", "")
        submittedImageRow.innerHTML = ""
    };



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

    document.addEventListener("DOMContentLoaded", () => {
        const modal = document.querySelector('[id="property-modal"]');
        modal.addEventListener("hidden.bs.modal", () => {
            clearFormImages();
        });
    });
})();


// Offer buttons
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
    };
    
    const acceptOfferButtons = document.getElementsByName("accept-offer-button")
    const acceptSubmitButton = document.getElementById("accept-offer-submit-button")
    
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
    });


    const acceptOfferOnSubmit = (id) => {
        const editForm = $('#accept-offer-form')
        editForm.unbind()
        editForm.submit( (e) => {
            
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
        editForm.unbind()
    };

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
    });


    const rejectOfferOnSubmit = (id, rowId) => {
        const editForm = $('#reject-offer-form')
        editForm.unbind()
        editForm.submit( (e) => {
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
        
    };


// Delete offer

    const deleteOfferButtons = document.getElementsByName("delete-offer-button")
    const deleteSubmitButton = document.getElementById("delete-offer-submit-button")

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
    });


    const deleteOfferOnSubmit = (id, rowId) => {
        const editForm = $('#delete-offer-form')
        editForm.unbind()
        editForm.submit( (e) => {
            
            e.preventDefault()
            e.stopPropagation()

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
    
    };


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
    });

    const contingentOfferOnSubmit = (id, textarea) => {
        const editForm = $('#contingent-offer-form')
        editForm.unbind()
        editForm.submit( (e) => {
            
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
    

    };

    const propertyFields = document.querySelectorAll('[id^="property-input"]');
    const propertySubmitButton = document.getElementById("create-property-modal-submit");
    
    propertyFields.forEach((element) => {
        element.addEventListener("change", () => {
            
            if (Array.from(propertyFields).map((el) => el.checkValidity()).reduce((f, s) => f && s)) {
                propertySubmitButton.disabled = false;
            } else {
                propertySubmitButton.disabled = true;
            }
    
            if (element.checkValidity()) {
                element.setAttribute("isvalid", "true");
                element.parentElement.querySelector(".invalid-text").style.display = "block"; 
            } else {
                try {
                    element.removeAttribute("isvalid");
                    element.parentElement.querySelector(".invalid-text").style.display = "none"; 
                } catch (e) {}
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
    };

    const acceptOfferRow = (element) => {
        address = document.getElementById("address-table-caller").innerHTML
        propRow = document.getElementById(address)
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