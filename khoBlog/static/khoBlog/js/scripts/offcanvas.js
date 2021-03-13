(function () {
    'use strict';

    document.querySelector('[data-bs-toggle="offcanvas"]').addEventListener('click', function () {
        document.querySelector('.offcanvas-collapse').classList.toggle('open');
        document.querySelector('body').classList.toggle('offcanvas-open');
    });
})();
