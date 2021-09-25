/* jshint esversion: 6 */
let isRoot = location.pathname === '/' && location.hash === '' && location.search === '';

if (isRoot) {
    let ele = document.getElementsByClassName('linkHome');
    for (let i = 0; i < ele.length; i++) {
        ele[i].classList.toggle('isHome');
    }
}
