(() => {

    const deletePropertyButtons = document.getElementsByName("offer-deleted-button")
    console.log(deletePropertyButtons)
    let submitButton = document.getElementById("delete-offer-submit-button")

    deletePropertyButtons.forEach((element) => {

        element.addEventListener("click", () => {
            let k = document.getElementById("delete-offer-modal-body-prompt")
            console.log(k)
            k.innerHTML = `Ertu viss um að þú viljir eyða þessu tilboði?`
        
            const listener = () => {
                id = element.getAttribute("data-id")
                rowId = `offer-id-${id}-row`
                deleteOfferOnSubmit(id, rowId)
        
                submitButton.removeEventListener("click", listener)
            }
            submitButton.addEventListener("click", listener)
        })
    })
    
    const deleteOfferOnSubmit = (id, rowId) => {
        const editForm = $("#delete-offer-form")
        editForm.unbind()
        editForm.submit( (e) => {
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
