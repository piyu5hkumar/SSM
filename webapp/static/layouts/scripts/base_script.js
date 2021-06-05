deactivateElement = (element) => {
    element.className = nav_link.className.slice(0, indexOfActive) + nav_link.className.slice(indexOfActive + 7,)
    element.style.color = "rgb(9,121,251)"
    element.style.backgroundColor = "white"
}

function activateElement(element) {
    element.className += " active"
    element.style.backgroundColor = "rgb(9,121,251)"
    element.style.color = "white"
}

function hoveredNavLink(hovered_nav_item) {

    if (!hovered_nav_item.className.includes("active") && !hovered_nav_item.className.includes("active")) {
        hovered_nav_item.style.color = "white"
        hovered_nav_item.style.backgroundColor = "rgb(168,210,223)"
    }
}

function notHoveredNavLink(hovered_nav_item) {
    if (!hovered_nav_item.className.includes("active")) {
        hovered_nav_item.style.color = "rgb(9,121,251)"
        hovered_nav_item.style.backgroundColor = "white"
    }
}

function doOnLoad() {
    selected_nav_link = document.getElementById("selected-nav-link").innerHTML
    nav_links = document.getElementsByClassName("nav-link")

    switch (selected_nav_link) {
        case "--": break;
        case "--": break;
        case "--": break;
        case "--": break;
        case "profile":
            activateElement(nav_links[4])
            break;
        default:
            activateElement(nav_links[0])
    }
}