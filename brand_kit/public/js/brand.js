// Hide splash immediately before anything renders
var style = document.createElement('style');
style.innerHTML = '.centered.splash { display: none !important; }';
document.head.appendChild(style);
