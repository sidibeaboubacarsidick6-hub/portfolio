(function () {
  "use strict";

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
      if (isOpen) {
        closeMenu();
      } else {
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

  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!prefersReduced && "IntersectionObserver" in window) {
    var sections = document.querySelectorAll("main > section[id]");
    sections.forEach(function (s) {
      s.style.opacity = "0";
      s.style.transform = "translateY(20px)";
      s.style.transition = "opacity 0.6s ease-out, transform 0.6s ease-out";
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.style.opacity = "1";
          e.target.style.transform = "translateY(0)";
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -40px 0px" });
    sections.forEach(function (s) { io.observe(s); });
  }
})();
