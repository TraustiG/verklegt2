(() => {

    const getPromises = () => {
        const modalClose  = new Promise((resolve) => {
            const modal = document.querySelector('[id="delete-offer-modal"]');
            console.log(modal)
            const listener = () => {
                modal.removeEventListener("hidden.bs.modal", listener)
                resolve(false)
            }
            modal.addEventListener("hidden.bs.modal", listener)
        })

        const submitPromise = new Promise((resolve) => {
            let submitButton = document.getElementById("delete-offer-submit-button")
            const listener = () => {
                submitButton.removeEventListener("click", listener)
                resolve(true)
            }
            submitButton.addEventListener("click", listener)
        })

        return [submitPromise, modalClose]
    }

    const deleteOfferOnSubmit = (id, rowId) => {

        $("#delete-offer-form").submit( function (e) {
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

    const deletePropertyButtons = document.getElementsByName("delete-offer")
    deletePropertyButtons.forEach((element) => {
        element.addEventListener("click", async () => {
            document.getElementById("delete-offer-modal-body-prompt").innerHTML = `Ertu viss um að þú viljir eyða þessu tilboði?`
            
            let id = element.getAttribute("data-id")
            let rowId = `offer-id-${id}-row`
            let submitForm = await Promise.race([getPromises()]) 
            if (!submitForm) { return }
    
            deleteOfferOnSubmit(id, rowId)
        })
    })
})()

