(function () {
  "use strict";

  document
    .querySelector("#top-navbar-collapse")
    .addEventListener("click", function () {
      document.querySelector(".offcanvas-collapse").classList.toggle("open");
      document.querySelector("body").classList.toggle("offcanvas-open");
    });
})();
