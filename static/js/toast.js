
//自定义弹框
function Toast(msg,duration){
    duration=isNaN(duration)?3000:duration;
    var m = document.createElement('div');
    m.innerHTML = msg;
    m.style.cssText="width: 30%;min-width: 150px;opacity: 0.7;height: 30px;color: rgb(245,255,250);line-height: 30px;text-align: center;border-radius: 5px;position: fixed;top: 80%;left: 35%;z-index: 999999;background: rgb(47, 79, 79);font-size: 18px;";
    document.body.appendChild(m);
    setTimeout(function() {
        var d = 0.5;
        m.style.webkitTransition = '-webkit-transform ' + d + 's ease-in, opacity ' + d + 's ease-in';
        m.style.opacity = '0';
        setTimeout(function() { document.body.removeChild(m) }, d * 1000);
    }, duration);
}
