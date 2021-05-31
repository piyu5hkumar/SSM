var o = 0.0
function loadButtons() {
    if (o < 1.0) {
        document.getElementsByClassName("hidden-buttons")[0].style.opacity = o.toString();
        o += 0.1
        setTimeout(loadButtons, 50);
    }
    else {
        document.getElementsByClassName("hidden-buttons")[0].style.pointerEvents = "auto";
    }
}
var i = 0, j = 0, k = 0;
var txt1 = 'WELCOME,';
var txt2 = 'It is a perfect place for your personal and public Journals.';
var txt3 = 'Free, as always.';
var speed = 10;
function typeWriterWelcome() {
    if (i < txt1.length) {
        document.getElementById("welcome").innerHTML += txt1.charAt(i);
        i++;
        setTimeout(typeWriterWelcome, speed);
    }
    else if (j < txt2.length) {
        document.getElementById("welcome_message").innerHTML += txt2.charAt(j);
        j++;
        setTimeout(typeWriterWelcome, speed);
    }
    else if (k < txt3.length) {
        document.getElementById("free").innerHTML += txt3.charAt(k);
        k++;
        setTimeout(typeWriterWelcome, speed);
    }
    else {
        loadButtons()
    }
}

window.onload = (event) => {
    typeWriterWelcome()
}