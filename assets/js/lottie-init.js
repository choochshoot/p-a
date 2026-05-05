function initLotties() {

  const lotties = document.querySelectorAll(".lottie-icon");

  lotties.forEach(el => {

    const path = el.dataset.path;
    const loop = el.dataset.loop === "true";
    const autoplay = el.dataset.autoplay !== "false";

    if (!path) return;

    const animation = lottie.loadAnimation({
      container: el,
      renderer: "svg",
      loop: loop,
      autoplay: false,
      path: path
    });

    // ============================
    // 🎯 SOLO METODOLOGÍA (COLOR FIX)
    // ============================
    if (path.includes("metodologia.json")) {

      const applyColors = () => {

        const paths = el.querySelectorAll("path");

        paths.forEach(p => {

          // 🎯 CONTORNO (más fino y elegante)
          if (p.getAttribute("stroke")) {
            p.setAttribute("stroke", "#93c5fd");
            p.setAttribute("stroke-width", "1.5");
          }

          // 🎯 RELLENO (más corporativo)
          if (p.getAttribute("fill") && p.getAttribute("fill") !== "none") {
            p.setAttribute("fill", "#3b82f6");
          }

          // 🎯 GLOW CONTROLADO (no neón)
          p.style.filter = "drop-shadow(0 2px 6px rgba(147,197,253,0.25))";

        });

      };

      // aplicar una vez
      setTimeout(applyColors, 300);

      // observar cambios internos del SVG (clave para Lottie)
      const mutationObserver = new MutationObserver(applyColors);

      mutationObserver.observe(el, {
        childList: true,
        subtree: true
      });

    }

    // ============================
    // 🎯 ANIMACIÓN POR SCROLL
    // ============================
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