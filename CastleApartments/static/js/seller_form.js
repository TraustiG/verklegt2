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

