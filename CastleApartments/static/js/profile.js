(() => {

    document.addEventListener("DOMContentLoaded", () => {
        
        const profileFields = document.querySelectorAll('[id^="profile-input"]');
        const profileSubmitButton = document.getElementById("edit-profile-modal-submit");
        
        profileFields.forEach((element) => {
            element.addEventListener("change", () => {
                
                if (Array.from(profileFields).map((el) => el.checkValidity()).reduce((f, s) => f && s)) {
                    profileSubmitButton.disabled = false;
                } else {
                    profileSubmitButton.disabled = true;
                }
        
                if (element.checkValidity()) {
                    element.setAttribute("isvalid", "true");
                    element.parentElement.querySelector(".invalid-text").style.display = "block"; 
                } else {
                    element.removeAttribute("isvalid");
                    element.parentElement.querySelector(".invalid-text").style.display = "none"; 
                }
            });
        });

        
        const modal = document.querySelector('[id="edit-profile-modal"]');
    
        modal.addEventListener("hidden.bs.modal", () => {
                modal.querySelector("form").reset();
            });
        

    });
})()