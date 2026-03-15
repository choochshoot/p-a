function initLotties() {

  const lottieElements = document.querySelectorAll(".lottie-icon");

  lottieElements.forEach((el, index) => {

    if (el.dataset.loaded) return;
    el.dataset.loaded = "true";

    const animation = lottie.loadAnimation({
      container: el,
      renderer: "svg",
      loop: el.dataset.loop === "true",
      autoplay: false,
      path: el.dataset.path,
      rendererSettings: {
        preserveAspectRatio: "xMidYMid meet"
      }
    });


    const observer = new IntersectionObserver(entries => {

      entries.forEach(entry => {

        if (entry.isIntersecting) {

          el.classList.add("reveal-icon");
          animation.play();

        } else {

          animation.pause();

        }

      });

    }, { threshold: 0.35 });

    observer.observe(el);

  });

}
