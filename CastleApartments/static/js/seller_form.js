
(() => {
    document.getElementsByName("role").forEach((element) => {
        element.addEventListener("change", () => {
            toggleSellerForm()
        })
    })
    
    
    const toggleSellerForm = () => {
        
        const sellerform = document.getElementById('seller-form')
        const selectedRole = document.querySelector('input[name="role"]:checked');
    
        if (selectedRole && selectedRole.value === 'seller') {
            sellerform.style.visibility = 'visible';
            sellerform.querySelectorAll('input, textarea, select').forEach(el => {
                el.disabled = false;
            })
    
        } else {
            sellerform.style.visibility = 'hidden';
            sellerform.querySelectorAll('input, textarea, select').forEach(el => {
                el.disabled = true;
            })
        }
    }
})()


const formFields = document.getElementsByClassName("buyer-form-field")
const sellerFormFields = document.getElementsByClassName("seller-form-field")
const registerButton = document.getElementById("register-form-submit-button")
registerButton.setAttribute("disabled", true)

    
Array.from(formFields).forEach((element) => {
    element.addEventListener("change", () => {
        if (Array.from(formFields).map((el) => el.checkValidity()).reduce((f, s) =>  f && s)) {
            registerButton.disabled = false
            element.setAttribute("isvalid", false)
        } else {
            registerButton.disabled = true
            element.setAttribute("isvalid", true)
        }
    })
})

Array.from(sellerFormFields).forEach((element) => {
    element.addEventListener("change", () => {
        if (Array.from(sellerFormFields).map((el) => el.checkValidity()).reduce((f, s) =>  f && s)) {
            registerButton.disabled = false
            element.setAttribute("isvalid", false)
        } else {
            registerButton.disabled = true
            element.setAttribute("isvalid", true)
        }
    })

})