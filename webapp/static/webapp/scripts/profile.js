function EnableEdit() {
    user_vals = document.getElementsByClassName("user-val")
    field_inputs = document.getElementsByClassName("field-input")

    for (i = 0; i < user_vals.length; i++) {
        field_value = user_vals[i].innerHTML
        user_vals[i].style.display = "none"

        if (field_inputs[i].type == "date")
            field_inputs[i].value = document.getElementById("formatted-date").innerHTML
        else
            field_inputs[i].value = field_value
        field_inputs[i].style.display = "block"
    }

    document.getElementById("edit_btn").style.display = "none"
    document.getElementById("save_btn").style.display = "block"
    document.getElementById("cancel_btn").style.display = "block"
}

function CancelEdits() {
    user_vals = document.getElementsByClassName("user-val")
    field_inputs = document.getElementsByClassName("field-input")

    for (i = 0; i < user_vals.length; i++) {
        user_vals[i].style.display = "block"
        field_inputs[i].style.display = "none"
    }
    document.getElementById("edit_btn").style.display = "block"
    document.getElementById("save_btn").style.display = "none"
    document.getElementById("cancel_btn").style.display = "none"
}

function SaveEdits() {
    form = document.getElementById("user-details")
    form.submit()
}