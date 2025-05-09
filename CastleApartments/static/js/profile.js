//resets edit profile modal when closed
document.addEventListener("DOMContentLoaded", () => {
    const modals = document.querySelectorAll('[id^="edit-profile-modal-"]');

    modals.forEach((modalEl) => {
        modalEl.addEventListener("hidden.bs.modal", () => {
            modalEl.querySelector("form").reset();
        });
    });
});