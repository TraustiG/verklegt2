(() => {
    try {
        document.getElementById("makeOffer-unavailable").addEventListener("click", () => {
            clicker()
        })
    } catch {}

    const clicker = () => {
        const el = document.getElementById("login-signup-dropdown-button")
        const dropdown = el.nextElementSibling
        el.classList.toggle("show")
        dropdown.classList.toggle("show")
        let pres = dropdown.toggleAttribute("data-bs-popper")
        if (pres) {
            dropdown.setAttribute("data-bs-popper","static")
        }
        el.toggleAttribute("aria-expanded")
    }
})()