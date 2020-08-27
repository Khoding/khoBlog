var mainHeading = document.title;

var isRoot = location.pathname == '/';

if (isRoot) {
    var ele = document.getElementsByClassName('linkHome');
    for (var i = 0; i < ele.length; i++) {
        ele[i].classList.toggle('isHome');
    }
}

document.getElementById('mainHeading').innerHTML = mainHeading;
