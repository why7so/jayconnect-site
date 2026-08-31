/* Jay Connect — поведение лендинга.
   Ванильный JS без сборки: сайт статический и деплоится как есть.
   Движение целиком выключается при prefers-reduced-motion. */

(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var hasIO = "IntersectionObserver" in window;

  /* ---------- шапка: фон и линия появляются после скролла ---------- */

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
     отписывается. Каскад внутри секции задаётся в разметке через --d. */

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

  /* ---------- переход по якорю ----------
     Перед прокруткой к разделу показываем всё, что в нём есть. Иначе блоки
     догоняют экран уже после того, как прокрутка закончилась, и переход
     между разделами выглядит рваным. */

  function revealInside(el) {
    if (!el) return;
    if (el.classList.contains("reveal")) el.classList.add("in");
    el.querySelectorAll(".reveal").forEach(function (r) { r.classList.add("in"); });
  }

  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    var id = a.getAttribute("href").slice(1);
    if (!id || id === "top") return; // ссылка на самый верх ничего не раскрывает
    a.addEventListener("click", function () {
      revealInside(document.getElementById(id));
    });
  });

  // прямой заход по ссылке вида /#pricing — раздел уже должен быть виден
  if (location.hash.length > 1) revealInside(document.getElementById(location.hash.slice(1)));

  /* ---------- кольцо подписки в макете приложения ----------
     Заполняется, только когда макет попал на экран: иначе анимация пройдёт
     впустую у тех, кто открыл страницу уже прокрученной. */

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

  /* ---------- липкая кнопка на телефонах ----------
     Появляется, когда кнопка первого экрана уехала вверх: дублировать её,
     пока она на виду, незачем. */

  var bar = document.getElementById("mobile-bar");
  var heroActions = document.querySelector(".hero-actions");

  function onBar() {
    bar.classList.toggle("show", heroActions.getBoundingClientRect().bottom < 0);
  }
  onBar();
  window.addEventListener("scroll", onBar, { passive: true });

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
