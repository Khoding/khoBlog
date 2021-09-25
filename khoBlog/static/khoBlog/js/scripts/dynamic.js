var isRoot = location.pathname === '/' && location.hash === '' && location.search === '';

if (isRoot) {
    var ele = document.getElementsByClassName('linkHome');
    for (var i = 0; i < ele.length; i++) {
        ele[i].classList.toggle('isHome');
    }
}
