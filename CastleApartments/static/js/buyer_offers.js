(() => {

    const deletePropertyButtons = document.getElementsByName("delete-offer")
    let submitButton = document.getElementById("delete-offer-submit-button")

    deletePropertyButtons.forEach((element) => {
        const listener = () => {
            document.getElementById("delete-offer-modal-body-prompt").innerHTML = `Ertu viss um að þú viljir eyða þessu tilboði?`
    
            id = element.getAttribute("data-id")
            rowId = `offer-id-${id}-row`
    
            submitButton.addEventListener("click", () => {
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
})();

(() => {
    const contingencyButtons = document.getElementByName("offer-contingency-button")
    Array.from(contingencyButtons).forEach((button) => {
        const listener = () => {
            
            button.removeEventListener("click", listener)
        }
        button.addEventListener("click", listener)
    })
})
