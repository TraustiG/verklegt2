priceButtons = document.getElementsByName("search-price-value-item")
searchPriceIndicator = document.getElementById("search-price-value-indicator")
searchPriceInput = document.getElementById("id_priceInput")

const visualToVal = (text) => text = text.split(" ")[0]*1000000

priceButtons.forEach((element) => {
    element.addEventListener("click", () => {
        let textValue = searchPriceIndicator.innerHTML.trim()
        if (textValue === "Verð") {
            searchPriceIndicator.toggleAttribute("disabled")
            if (element.classList.contains("-min-")) {
                    searchPriceIndicator.innerHTML = element.innerHTML + " +"
                    searchPriceInput.value = visualToVal(element.innerHTML) + "-"
            } else {
                    searchPriceIndicator.innerHTML = "0 - " + element.innerHTML
                    searchPriceInput.value = "-" + visualToVal(element.innerHTML)
            }
        } else if (textValue.includes("+")) {
            if (element.classList.contains("-min-")) {
                 textValue = element.innerHTML + " +"
                searchPriceInput.value = visualToVal(element.innerHTML) + "-"
            } else {
                let prev = textValue
                searchPriceIndicator.innerHTML = textValue.replace("+","- ") + element.innerHTML
                searchPriceInput.value = visualToVal(prev) + "-" + visualToVal(element.innerHTML)
            }
        } else {
            let parts = textValue.split(" - ")
            if (element.classList.contains("-min-")) {
                parts[0] = element.innerHTML
            } else {
                parts[1] = element.innerHTML
            }
            searchPriceIndicator.innerHTML = parts.join(" - ")
            searchPriceInput.value = parts.map((val) => {
                return visualToVal(val)
            }).join("-")
            
        }
    })
})


searchPriceIndicator.addEventListener("click", () => {
    searchPriceIndicator.toggleAttribute("disabled")
    searchPriceIndicator.innerHTML = "Verð"
})

const sorter = () => {
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
}
let openFilterSaverButton = document.getElementById("open-filter-saver-button")
let saveFilterButton = document.getElementById("filter-saver-button")

openFilterSaverButton.addEventListener("click", () => {
    const listener = () => {
        saveFilter()
        console.log("saved")
        saveFilterButton.removeEventListener("click", listener)
        openFilterSaverButton.click()
    }
    saveFilterButton.addEventListener("click", listener)
})

const saveFilter = () => {
    const area = document.getElementById("id_areaSelect").value
    const type = document.getElementById("id_typeSelect").value
    const price = document.getElementById("id_priceInput").value
    const desc = document.getElementById("id_descInput").value
    const name = document.getElementById("id_filterName").value
    let dropdown = document.getElementById("dropdownCheck").value
    dropdown = "on" ? "True" : "False"
    let form = $("#save-filter-form")
    console.log(area, type, price, desc, name, dropdown)
    form.submit( function (e) {
        e.preventDefault()
        $.ajax({
            type: "POST",
            url: "/filters/",
            data: {
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                monitor: dropdown,
                area: area,
                price: price,
                re_type: type,
                name: name,
                desc: desc,
            }
        })
    })
}
            


const getFields = () => {
    const area = document.getElementById("id_areaSelect")
    const type = document.getElementById("id_typeSelect")
    const price = document.getElementById("id_priceInput")
    const desc = document.getElementById("id_descInput")
    const dropdown = document.getElementById("dropdownCheck")
    const name = document.getElementById("id_filterName")
    return [area, type, price, desc, dropdown, name]
}

const elements = [...document.querySelectorAll(".saved-filter")]

if (elements) {
    elements.forEach((element) => {
        element.addEventListener("click", () => {
            useFilter(element)
        })
    })
}

const useFilter = (element) => {
    let area = element.getAttribute("data-area")
    let type = element.getAttribute("data-re_type")
    let price = element.getAttribute("data-price")
    let desc = element.getAttribute("data-desc")
    let name = element.getAttribute("data-name")
    const filter = JSON.parse(element.getAttribute("filter"))
    let query = "/search/?"
    for (let [key, value] of Object.entries(filter)) {
        if (value) {
            let field = document.getElementById(`id_${key}`)
            field.value = value
            query = query.concat(`${key}=${value}&`)
        }
    }
    element.setAttribute("href", query)
    //element.click()
}