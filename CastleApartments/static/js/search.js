document.getElementById("orderBySelect")
    .addEventListener("change", (event) => {
        sortItems(event)
})

const sortItems = (event) => {
    const elements = [...document.querySelectorAll(".real-estate-card")]
    const parentElement = elements[0].parentNode
    const option = parseInt(event.target.value)

    const asc = !(option%2 === 0) // && option !== 0  ??
    const isNumeric = (option < 3)

    const selector = (option, element) => {
        switch(option) {
            case 0:
                return element.id
            case 1:
            case 2:
                let price = element.querySelector("b.price").innerText 
                price = parseInt(price.split(" ")[0].replace(".",""))
                return price
            case 3:
            case 4:
                return element.querySelector("h5.address").innerText //address desc   
        }
    }
    const collator = new Intl.Collator("is", {numeric: isNumeric, sensitivity: "base"})

    elements.sort((elementA, elementB) => {
        const [first, second] = asc ? [elementA, elementB] : [elementB, elementA]
        const firstValue = selector(option, first)
        const secondValue = selector(option, second)
        return collator.compare(firstValue, secondValue)
    }).forEach(element => parentElement.appendChild(element))
}