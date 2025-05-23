(() => {

    const hiddenPaymentOptions = document.querySelectorAll(".hidden-payment-option")
    const hiddenPaymentInformation = document.querySelectorAll(".hidden-payment-information")
    const paymentPicker = document.getElementById("payment-option-select")

    
    const entryContinueButton = document.querySelector("#entry-payment-modal-continue-button")
    const optionContinueButton = document.querySelector("#option-payment-modal-continue-button")
    
    let paymentOptionFields = new Set([])
    const paymentContactFields = document.querySelectorAll('[id^="payment-contact"]')
    let tempForm = Array.from(document.forms).filter((f) => f.id === "temp-input-form")[0]
    
    
    entryContinueButton.addEventListener("click", () => {
        addContactInformation()
    })
    
    optionContinueButton.addEventListener("click", () => {
        addPaymentInformation(paymentPicker.value)
        let submitterButton = document.querySelector('[id="information-overview-modal-continue-button"]')
        const listener = () => {
            const conf = new JSConfetti()
            conf.addConfetti()

            let id = document.querySelector('[id="payment-form-actual-offer-id"]').value
            let rowElement = document.getElementById(`offer-id-${id}-row`)
            rowElement.parentNode.removeChild(rowElement)

            formSubmitter(id)
            submitterButton.removeEventListener("click", listener)
        }
        submitterButton.addEventListener("click", listener)
    })

    const formSubmitter = (id) => {
        let form = $("#offer-payment-form")
        form.unbind()
        form.submit( (e) => {
            
            e.preventDefault()
            let data = form.serialize()
            
            $.ajax({
                type: "POST",
                url: `/payments/${id}`,
                data: data,
            })
        })
     
    }
    

    paymentContactFields.forEach((element) => {
        element.addEventListener("change", () => {
            element.setAttribute("isvalid", element.checkValidity())
            if (Array.from(paymentContactFields).map((el) => el.checkValidity()).reduce((f, s) =>  f && s)) {
                entryContinueButton.disabled = false
            } else {
                entryContinueButton.disabled = true
            }
        })
    })
    
    const addContactInformation = () => {
        paymentContactFields.forEach((element) => {
            let queryString = `[id="payment-form-offer-property-${element.name}"]`
            document.querySelector(queryString).innerHTML = element.value
        })
    }
    
    paymentPicker.addEventListener("change", (event) => {
        paymentFormToggle(event.target.value)
        paymentInformationToggle(event.target.value)
        paymentFieldsToggle(event.target.value)
    })
    
    const paymentFormToggle = (option) => {
        hiddenPaymentOptions.forEach((element) => {
            if (element.classList.contains(option)) {
                element.style.display = ""
            } else {
                element.style.display = "none"
            }
        })
    }
    
    const paymentInformationToggle = (option) => {
        hiddenPaymentInformation.forEach((element) => {
            if (element.classList.contains(option)) {
                element.style.display = ""
            } else {
                element.style.display = "none"
            }
        })
    }
    
    const paymentFieldsToggle = (option) => {
        let idName = `[id^="payment-option-${option}"]`
        let optionFields = document.querySelectorAll(idName)
    
        optionFields.forEach((element, i) => {
            paymentOptionFields.add(element)
            element.addEventListener("change", (event) => {
                element.setAttribute("isvalid", element.checkValidity())
                if (Array.from(optionFields).map((el) => el.checkValidity()).reduce((f, s) =>  f && s)) {
                    let confirmElName = `[id="payment-form-offer-property-${event.target.name}"]`
                    try {
                        document.querySelector(confirmElName).innerHTML = event.target.value
                    } catch (err) { }
                    optionContinueButton.disabled = false
                } else {
                    optionContinueButton.disabled = true
                }
            })
        })
        
    }
    
    const makePaymentButtons = document.querySelectorAll('[name="offer-accepted-button"]')
    const morePaymentButtons = document.querySelectorAll('[name="offer-contingency-button"]')
    
    const formSetter = (element) => {
        element.addEventListener("click", () => {
            resetForm()
            let input = document.querySelector('[id="payment-form-actual-offer-id"]')
            let imageDiv = document.querySelector('[id="payment-form-image"]')
            imageDiv.innerHTML = ""
            let image = document.createElement("img")
            image.src = element.getAttribute("data-image")
            image.setAttribute("height", "250rem")
            imageDiv.appendChild(image)
            let promptDiv = document.querySelector('[id="contingency-modal-body-message"]')
            let contingencyMessage = element.getAttribute("data-offer-message")

            promptDiv.innerHTML = contingencyMessage ? contingencyMessage : ""
            
            input.value = element.getAttribute("data-id")
            input.setAttribute("value", element.getAttribute("data-id"))
    
            let sub_header_items = ["street-name", "offer-amount", "zip-city", "type", "listing-price"]
            sub_header_items.forEach((str) => {
                let elements = document.getElementsByName(`payment-form-offer-property-${str}`)
                elements.forEach((el) => {
                    if (str==="zip-city") {
                        let zip = element.getAttribute("data-zip")
                        let city = element.getAttribute("data-city")
                        let temp = `${zip} ${city}`
                        el.innerHTML = temp
                    } else {
                        let vis;
                        temp = element.getAttribute(`data-${str}`)
                        if (str==="offer-amount") {
                            vis = `Söluverð ${temp} kr.`
                        } else if (str==="listing-price") {
                            vis = `Skráð ${temp} kr.`
                        } else { vis = temp }
                        el.innerHTML = vis
                    }
                })
            })
    
        })
    }
    
    makePaymentButtons.forEach((element) => formSetter(element))
    morePaymentButtons.forEach((element) => formSetter(element))
        
        
    ////  tester takki
    // document.getElementById("payment-tester-fill-payments").addEventListener("click", () => {
    //     addContactInformation()
    // }
    // )
    
    const addPaymentInformation = (option) => {
        let input = document.querySelector('[id="payment-form-actual-payment-option"]')
        input.value = option
        input.setAttribute("value", option)
    
        const queryString = `[id^="payment-option-${option}"]`
        informationFields = document.querySelectorAll(queryString)
        informationFields.forEach((field) => {
            try {
                document.getElementById(`payment-form-${option}-${field.name}`).innerHTML = tempForm[field.name].value
            } catch (err) { }
        })
    
    }
    
    const resetForm = () => {
        paymentPicker.value = ""
        paymentPicker.setAttribute("value", "")
        entryContinueButton.disabled = true
        optionContinueButton.disabled = true
        paymentContactFields.forEach((el) => {
            el.value = ""
            el.setAttribute("value", "")
            el.removeAttribute("isvalid")
        })
        paymentOptionFields.forEach((el) => {
            el.value = ""
            el.setAttribute("value", "")
            el.removeAttribute("isvalid")
        })
        hiddenPaymentOptions.forEach((el) => {
            el.style.display = "none"
        })
    }
})()