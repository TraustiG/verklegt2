function cycleTheme() {
    const currentTheme = localStorage.getItem("theme") || "light";
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

    if (prefersDark) {
        // Auto (dark) -> Light -> Dark
        if (currentTheme === "dark") {

            setTheme("light");
            //document.getElementById("footer-img").setAttribute("src", "/static/images/logo.png")
        } else {
            setTheme("dark");
            //document.getElementById("footer-img").setAttribute("src", "/static/images/logo-darkmode.png")
        }
    } else {
        // Auto (light) -> Dark -> Light
        if (currentTheme === "light") {
            setTheme("dark");
            //document.getElementById("footer-img").setAttribute("src", "/static/images/logo-darkmode.png")
        } else {
            setTheme("light");
            //document.getElementById("footer-img").setAttribute("src", "/static/images/logo.png")
        }
    }
}

const init = (function initTheme() {
    const currentTheme = localStorage.getItem("theme");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

    if (prefersDark) {
        const link = document.querySelector("link[rel*='icon']")
        link.setAttribute("href", "/static/images/logo-darkmode.png")
    }
    currentTheme ? setTheme(currentTheme) : setTheme("light");
})()


function setTheme(mode) {
    if (mode !== "light" && mode !== "dark") {
        console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
        mode = "light";
    }
    document.documentElement.dataset.theme = mode;
    localStorage.setItem("theme", mode);
}