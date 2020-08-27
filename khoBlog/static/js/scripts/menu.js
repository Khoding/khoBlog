/* Scripts for the menu and the ones that are activated IN the menu */
function w3_open() {
    if (window.matchMedia('(min-width: 600px)').matches) {
        document.getElementById('menuSidebar').style.width = '25%';
        document.getElementById('main').style.marginLeft = '25%';
    }
    document.getElementById('menuSidebar').style.display = 'block';
    document.getElementById('overlayMenu').style.display = 'block';
    document.getElementById('openMenu').style.margin = '-50px 0';
}

function w3_close() {
    document.getElementById('main').style.marginLeft = '0%';
    document.getElementById('menuSidebar').style.display = 'none';
    document.getElementById('overlayMenu').style.display = 'none';
    document.getElementById('openMenu').style.display = 'inline-block';
    document.getElementById('openMenu').style.margin = '0';
}

/* Document Outline */
function showElements() {
    let domStyle = document.getElementById('domStylee');
    if (domStyle) {
        document.body.removeChild(domStyle);
        return;
    }

    domStyle = document.createElement('style');
    domStyle.setAttribute('id', 'domStylee');
    domStyle.append(
        ['* { color:#0f0!important;outline:solid #f00 1px!important; background-color: rgba(255,0,0,.2) !important; }'],
        ['* * { background-color: rgba(0,255,0,.2) !important; }'],
        ['* * * { background-color: rgba(0,0,255,.2) !important; }'],
        ['* * * * { background-color: rgba(255,0,255,.2) !important; }'],
        ['* * * * * { background-color: rgba(0,255,255,.2) !important; }'],
        ['* * * * * * { background-color: rgba(255,255,0,.2) !important; }'],
        ['* * * * * * * { background-color: rgba(255,0,0,.2) !important; }'],
        ['* * * * * * * * { background-color: rgba(0,255,0,.2) !important; }'],
        ['* * * * * * * * * { background-color: rgba(0,0,255,.2) !important; }'].join()
    );
    document.body.appendChild(domStyle);
}

/* Light Mode */
const app = document.getElementsByClassName('app')[0];

const toggleMode = () => {
    app.classList.toggle('light');
};
