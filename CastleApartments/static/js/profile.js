(() => {
    document.addEventListener("DOMContentLoaded", () => {
        const modal = document.querySelector('[id="edit-profile-modal"]');
    
        modal.addEventListener("hidden.bs.modal", () => {
                modal.querySelector("form").reset();
            });
        });
})()