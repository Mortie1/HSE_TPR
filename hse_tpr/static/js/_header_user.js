const optionMenu = document.querySelector(".select-menu"),
    selectBtn = optionMenu.querySelector(".select-btn"),
    options = optionMenu.querySelectorAll(".option"),
    sBtn_text = optionMenu.querySelector(".sBtn-text");

    

selectBtn.addEventListener("click", () =>
    optionMenu.classList.toggle("active")
);

options.forEach((option) => {
    option.addEventListener("click", () => {
        // let selectedOption = option.querySelector(".option-text").innerText;
        // sBtn_text.innerText = selectedOption;
        window.location = option.getElementsByTagName("a")[0].href;
        optionMenu.classList.remove("active");
    });
});


// setTimeout(() => {
//     document.querySelector(".options").style.cssText = "animation-name: fadeInDown;\
// -webkit-animation-name: fadeInDown;\
// animation-duration: 0.35s;\
// animation-fill-mode: both;\
// -webkit-animation-duration: 0.35s;\
// -webkit-animation-fill-mode: both;";
// }, 1000);
