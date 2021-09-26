/* jshint esversion: 6 */

function cssCheck() {
  let domStyle = document.getElementById("domStylee");
  if (domStyle) {
    document.body.removeChild(domStyle);
    return;
  }
  domStyle = document.createElement("style");
  domStyle.setAttribute("id", "domStylee");
  domStyle.append(
    [
      "* { color:#0f0!important;outline:solid #f00 1px!important; background-color: rgba(255,0,0,.2) !important; }",
    ],
    ["* * { background-color: rgba(0,255,0,.2) !important; }"],
    ["* * * { background-color: rgba(0,0,255,.2) !important; }"],
    ["* * * * { background-color: rgba(255,0,255,.2) !important; }"],
    ["* * * * * { background-color: rgba(0,255,255,.2) !important; }"],
    ["* * * * * * { background-color: rgba(255,255,0,.2) !important; }"],
    ["* * * * * * * { background-color: rgba(255,0,0,.2) !important; }"],
    ["* * * * * * * * { background-color: rgba(0,255,0,.2) !important; }"],
    [
      "* * * * * * * * * { background-color: rgba(0,0,255,.2) !important; }",
    ].join(),
    document.body.appendChild(domStyle)
  );
}
