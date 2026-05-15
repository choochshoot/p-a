function initLotties() {

  if (!window.lottie) {
    console.warn("lottie-web no esta disponible; se omiten animaciones Lottie.");
    return;
  }

  const lotties = document.querySelectorAll(".lottie-icon");

  const loadLottie = (el) => {
    if (el.dataset.loaded === "true") return;

    const path = el.dataset.path;
    const loop = el.dataset.loop === "true";

    if (!path) return;

    el.dataset.loaded = "true";

    const animation = lottie.loadAnimation({
      container: el,
      renderer: "svg",
      loop: loop,
      autoplay: false,
      path: path
    });

    // ============================
    // SOLO METODOLOGIA (COLOR FIX)
    // ============================
    if (path.includes("metodologia.json")) {

      const applyColors = () => {

        const paths = el.querySelectorAll("path");

        paths.forEach(p => {

          // Contorno mas fino y elegante
          if (p.getAttribute("stroke")) {
            p.setAttribute("stroke", "#93c5fd");
            p.setAttribute("stroke-width", "1.5");
          }

          // Relleno mas corporativo
          if (p.getAttribute("fill") && p.getAttribute("fill") !== "none") {
            p.setAttribute("fill", "#3b82f6");
          }

          // Glow controlado
          p.style.filter = "drop-shadow(0 2px 6px rgba(147,197,253,0.25))";

        });

      };

      setTimeout(applyColors, 300);

      const mutationObserver = new MutationObserver(applyColors);

      mutationObserver.observe(el, {
        childList: true,
        subtree: true
      });

    }

    const playbackObserver = new IntersectionObserver(entries => {

      entries.forEach(entry => {

        if (entry.isIntersecting) {
          el.classList.add("reveal-icon");
          animation.play();
        } else {
          animation.pause();
        }

      });

    }, { threshold: 0.35 });

    playbackObserver.observe(el);
  };

  const loadObserver = new IntersectionObserver(entries => {

    entries.forEach(entry => {

      if (!entry.isIntersecting) return;

      loadLottie(entry.target);
      loadObserver.unobserve(entry.target);

    });

  }, {
    root: null,
    rootMargin: "240px 0px",
    threshold: 0
  });

  lotties.forEach(el => loadObserver.observe(el));

}
