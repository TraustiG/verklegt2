function cycleTheme() {
    const currentTheme = localStorage.getItem("theme") || "light";
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

    if (prefersDark) {
        if (currentTheme === "dark") {

            setTheme("light");
        } else {
            setTheme("dark");
        }
    } else {
        if (currentTheme === "light") {
            setTheme("dark");
        } else {
            setTheme("light");
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