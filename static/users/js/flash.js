var closeBtn = document.querySelector(".close");

closeBtn.addEventListener("click", (event) => {
    let parent = closeBtn.parentNode;
    parent.classList.add("hide-error");
})
