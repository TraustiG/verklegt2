document.getElementById("id_role_0")
    .addEventListener("change", (event) => {
        toggleSellerForm(event)
})



const toggleSellerForm = (event) => {
    
    const sellerform = document.getElementById('seller-form')
    const selectedRole = event.target

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

