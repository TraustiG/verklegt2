
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
const buyerRadio = document.getElementById("id_role_0")
const sellerRadio = document.getElementById("id_role_1")
const individualRadio = document.getElementById("id_type_0")
const reaRadio = document.getElementById("id_type_1")
const passwordFields = [...document.querySelectorAll('input[id^="id_password"]')]
const passwordCopy = document.getElementById("id_password2")

registerButton.setAttribute("disabled", true)

const passwordCheck = () => {
    if (passwordFields.reduce((f,s) => f.value===s.value)) {
        return true
    }
    if (passwordCopy.value != "") {
        passwordCopy.setAttribute("isvalid", false)
    }
    return false
}
    
Array.from(formFields).concat([buyerRadio, sellerRadio]).forEach((element) => {
    element.addEventListener("change", () => {
        element.setAttribute("isvalid", element.checkValidity())

        if (Array.from(formFields).map((el) => el.checkValidity()).reduce((f, s) =>  f && s)
        && (buyerRadio.checked || sellerRadio.checked) && passwordCheck()) {
            if (sellerRadio.checked) {
                checkSeller()
            } else {
                registerButton.disabled = false
            }
        } else {
            registerButton.disabled = true
        }
    })
})

passwordFields.forEach((field) => {
    field.addEventListener("change", () => {
        passwordCheck()
    })
})

Array.from(sellerFormFields).concat([individualRadio,reaRadio]).forEach((element) => {
    element.addEventListener("change", () => {
        element.setAttribute("isvalid", element.checkValidity())
        checkSeller()
    })
})

const checkSeller = () => {
        if (Array.from(sellerFormFields).map((el) => el.checkValidity()).reduce((f, s) =>  f && s)
        && (individualRadio.checked || reaRadio.checked)) {
            registerButton.disabled = false
        } else {
            registerButton.disabled = true
        }
}