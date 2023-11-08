function initClickPreview() {
    let displayContainer = document.getElementById("display-container");
    let display = document.getElementById("display");
    let loadingIcon = "https://upload.wikimedia.org/wikipedia/commons/6/68/Spinner_indicator.png";
    display.src = loadingIcon;
    displayContainer.addEventListener("click", function(e) {
        displayContainer.style.display = "none";
        display.src = loadingIcon;
        display.setAttribute("title", "");
        // document.location.hash = '';
        history.back();
    });

    let container = document.getElementById("content");
    let images = container.getElementsByTagName("img");
    for (var i = 0; i < images.length; i++) {
        images[i].onclick = function(e) {
            e.preventDefault();
            let image = e.target;
            displayContainer.style.display = null;
            display.src = image.parentElement.href;
            display.setAttribute("title", image.title);
            // document.location.hash = image.id;
            history.pushState({}, "", "#"+image.id);
        }
    }

    if (document.location.hash != "") {
        let hash = document.location.hash.replace('#', '');
        document.location.hash = "";
        let img = document.getElementById(hash);
        if (img) img.click();
    }

}


window.onload = function() {
    initClickPreview();
}
