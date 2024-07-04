const btns = document.querySelectorAll(".nav-btn");
        const slides = document.querySelectorAll(".video-slide");
        const contents = document.querySelectorAll(".content");
        let start = -1;

        var sliderNav = function (manual) {
            btns.forEach((btn) => {
                btn.classList.remove("active");
            });

            slides.forEach((slide) => {
                slide.classList.remove("active");
                slide.pause()
            });

            contents.forEach((content) => {
                content.classList.remove("active");
            });

            btns[manual].classList.add("active");
            slides[manual].classList.add("active");
            slides[manual].currentTime = 0;
            slides[manual].play()
            contents[manual].classList.add("active");
            return manual;
        };
        //  Automatic slider
        window.onload = sliderAutomatic();
        function sliderAutomatic() {

            if (start < slides.length - 1) {
                start++;
            }
            else {
                start = 0;
            }
            // console.log(start);
            start = sliderNav(start);
        };

        let interval = setInterval(sliderAutomatic, 8000);

        // clearInterval(interval);

        // On click slider
        btns.forEach((btn, i) => {
            btn.addEventListener("click", () => {
                start = sliderNav(i);
            });


        });
