function showPassword() {
    var checkBox = document.getElementById("show_password");
    var password_field = document.getElementById("password_field");
    if (checkBox.checked == true) {
        password_field.type = "text"
    } else {
        password_field.type = "password"
    }
}

function validateForm() {
    var form = document.forms["signup_form"];
    if (form["re_password"].value != form["password"].value) {
        $('#ModalCenter').modal('show')
        console.log("fully executed")
        return false
    }
    return true
}