/* Jay Connect — поведение лендинга.
   Ванильный JS без сборки: сайт статический и деплоится как есть.
   Движения минимум, и оно целиком выключается при prefers-reduced-motion. */

(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var hasIO = "IntersectionObserver" in window;

  /* ---------- шапка: линия и фон появляются после скролла ---------- */

  var nav = document.getElementById("nav");
  var burger = document.getElementById("burger");

  function onScroll() {
    nav.classList.toggle("scrolled", window.scrollY > 8);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---------- меню на узких экранах ---------- */

  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });

  document.querySelectorAll("#mobile-menu a").forEach(function (a) {
    a.addEventListener("click", function () {
      nav.classList.remove("open");
      burger.setAttribute("aria-expanded", "false");
    });
  });

  /* ---------- появление блоков ----------
     Один наблюдатель на все .reveal: элемент показывается один раз и сразу
     отписывается, чтобы не считать пересечения до конца жизни страницы.
     Каскад внутри секции задаётся в разметке через --d. */

  var revealables = document.querySelectorAll(".reveal");

  if (reduced || !hasIO) {
    revealables.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("in");
        io.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.1 });

    revealables.forEach(function (el) { io.observe(el); });
  }

  /* ---------- кольцо подписки в макете приложения ----------
     Заполняется, только когда макет реально попал на экран: иначе анимация
     проходит впустую у тех, кто открыл страницу уже прокрученной. */

  var phone = document.getElementById("phone");

  if (reduced || !hasIO) {
    phone.classList.add("is-live");
  } else {
    var phoneIO = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting) return;
      phone.classList.add("is-live");
      phoneIO.disconnect();
    }, { threshold: 0.3 });
    phoneIO.observe(phone);
  }

  /* ---------- вопросы ---------- */

  document.querySelectorAll(".qa-q").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var qa = btn.parentElement;
      var willOpen = !qa.classList.contains("open");
      // одновременно раскрыт только один вопрос
      document.querySelectorAll(".qa.open").forEach(function (other) {
        other.classList.remove("open");
      });
      qa.classList.toggle("open", willOpen);
    });
  });

  /* ---------- год в подвале ---------- */

  document.getElementById("year").textContent = new Date().getFullYear();
})();
