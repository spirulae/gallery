function initClickPreview() {
    let displayContainer = document.getElementById("display-container");
    let display = document.getElementById("display");
    let loadingIcon = "https://upload.wikimedia.org/wikipedia/commons/6/68/Spinner_indicator.png";
    display.src = loadingIcon;
    displayContainer.addEventListener("click", function(e) {
        displayContainer.style.display = "none";
        display.src = loadingIcon;
        display.setAttribute("alt", "");
        display.setAttribute("title", "");
        // document.location.hash = '';
        history.back();
    });

    let container = document.getElementById("content");
    let images = container.getElementsByTagName("img");
    for (var i = 0; i < images.length; i++) {
        images[i].setAttribute("prev", images[Math.max(i-1, 0)].id);
        images[i].setAttribute("next", images[Math.min(i+1, images.length-1)].id);
        images[i].onclick = function(e) {
            e.preventDefault();
            let image = e.target;
            displayContainer.style.display = null;
            display.src = image.parentElement.href;
            display.setAttribute("alt", image.id);
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

    document.body.addEventListener("keydown", function(event) {
        let cur_id = display.getAttribute("alt");
        if (cur_id === "") return;
        let cur_image = document.getElementById(cur_id);
        if (event.key == "ArrowLeft") {
            history.back();
            document.getElementById(cur_image.getAttribute("prev")).click();
        }
        if (event.key == "ArrowRight") {
            history.back();
            document.getElementById(cur_image.getAttribute("next")).click();
        }        
    });

}


window.onload = function() {
    initClickPreview();
}
