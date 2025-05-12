(() => {

    const deletePropertyButtons = document.getElementsByName("delete-offer")
    let submitButton = document.getElementById("delete-offer-submit-button")

    deletePropertyButtons.forEach((element) => {
        element.addEventListener("click", async () => {
            document.getElementById("delete-offer-modal-body-prompt").innerHTML = `Ertu viss um að þú viljir eyða þessu tilboði?`

            id = element.getAttribute("data-id")
            rowId = `offer-id-${id}-row`
    
            submitButton.addEventListener("click", () => {
                deleteOfferOnSubmit(id, rowId)
            })
        })
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
})()


