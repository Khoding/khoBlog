/* jshint esversion: 6 */

void (function () {
    let i, a, s;
    a = document.getElementsByTagName('link');
    for (i = 0; i < a.length; i++) {
        s = a[i];
        if (s.rel.toLowerCase().indexOf('stylesheet') >= 0 && s.href) {
            const h = s.href.replace(/(&|%5C?)forceReload=\d+/, '');
            s.href = h + (h.indexOf('?') >= 0 ? '&' : '?') + 'forceReload=' + new Date().valueOf();
        }
    }
})();
