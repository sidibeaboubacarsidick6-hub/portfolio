(function () {
  "use strict";

  // === MENU MOBILE ===
  var toggle = document.getElementById("menu-toggle");
  var menu = document.getElementById("mobile-menu");
  var iconOpen = document.getElementById("menu-icon-open");
  var iconClose = document.getElementById("menu-icon-close");

  function closeMenu() {
    if (!menu || !toggle) return;
    menu.classList.add("hidden");
    if (iconOpen) iconOpen.classList.remove("hidden");
    if (iconClose) iconClose.classList.add("hidden");
    toggle.setAttribute("aria-expanded", "false");
  }

  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var isOpen = !menu.classList.contains("hidden");
      if (isOpen) { closeMenu(); }
      else {
        menu.classList.remove("hidden");
        if (iconOpen) iconOpen.classList.add("hidden");
        if (iconClose) iconClose.classList.remove("hidden");
        toggle.setAttribute("aria-expanded", "true");
      }
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", closeMenu);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });
  }

  // === SCROLL REVEAL (respecte prefers-reduced-motion) ===
  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (prefersReduced) return;

  var els = document.querySelectorAll("[data-reveal]");
  if (!els.length || !("IntersectionObserver" in window)) return;

  els.forEach(function (el) {
    el.style.opacity = "0";
    el.style.transform = "translateY(24px)";
    el.style.transition = "opacity 0.7s cubic-bezier(0.22, 1, 0.36, 1), transform 0.7s cubic-bezier(0.22, 1, 0.36, 1)";
    var delay = el.getAttribute("data-reveal-delay") || "0";
    el.style.transitionDelay = delay + "ms";
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.style.opacity = "1";
        e.target.style.transform = "translateY(0)";
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.1, rootMargin: "0px 0px -60px 0px" });

  els.forEach(function (el) { io.observe(el); });
})();
