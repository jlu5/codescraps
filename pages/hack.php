<html>
<head>
<title>Blog</title>
<link rel="stylesheet" href="hack.css">
</head>
<body>
<br>
<h1 id="t1" class="entry">LOOKING UP YOUR IP ADDRESS</h1>
<h1 id="t2">
</h1>
<h1 id="t3">
</h1>
<h1 id="t4">
</h1>
<h1 id="t5">
</h1>
<script>
var dcount = 600;
function route(id){
    if (id == "t1") {
        writeText()
    } else if (id == "t5") {
        setTimeout(function () {freezeUp()}, 200)
    }
}

function addDots(id){
    var rnd = Math.floor((Math.random() * 4) + 4)
    var dots = {}
    dots[id] = setInterval(function () {
    document.getElementById(id).innerHTML = document.getElementById(id).innerHTML + ".";
    }, dcount)
    setTimeout(function () {clearInterval(dots[id]); route(id)}, rnd*dcount)
}
addDots("t1")
function writeText(){
    document.getElementById("t2").innerHTML = '<span class="entry">IP ADDRESS FOUND:</span> <?php echo $_SERVER['REMOTE_ADDR'];?>';
    document.getElementById("t3").innerHTML = '<span class="entry">OPERATING SYSTEM FOUND:</span> ' + navigator.platform;
    document.getElementById("t4").innerHTML = '<span class="entry">USER AGENT STRING:</span> ' + navigator.userAgent;
    setTimeout(function () {document.getElementById("t5").innerHTML = "OPERATING SYSTEM VULNERABLE<br>LAUNCHING PAYLOAD "}, 900)
    addDots("t5")
}

function freezeUp(){
    var overlay=document.createElement('div');
    document.title = document.title+' (Not Responding)';
    overlay.setAttribute('style','cursor:wait;position:fixed;width:100%;height:100%;opacity:0.8;z-index:5000000;top:0;left:0;background-color:#FFFFFF;');
    document.body.appendChild(overlay);
}
</script>
</body>
</html>