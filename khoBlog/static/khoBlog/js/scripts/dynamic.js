/* jshint esversion: 6 */

const isRoot = location.pathname === '/' && location.hash === '' && location.search === '';

if (isRoot) {
    const ele = document.getElementsByClassName('linkHome');
    for (let i = 0; i < ele.length; i++) {
        ele[i].classList.toggle('isHome');
    }
}
