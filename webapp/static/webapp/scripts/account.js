function EnableEditAccount() {
    console.log("trying")
    console.log($("#mm"))
    $('#mm').toast('show')
    console.log("trieeeeed")
    // user_vals = document.getElementsByClassName("user-val")
    // field_inputs = document.getElementsByClassName("account-field-input")

    // for (i = 0; i < user_vals.length; i++) {
    //     field_value = user_vals[i].innerHTML
    //     user_vals[i].style.display = "none"

    //     field_inputs[i].value = field_value
    //     field_inputs[i].style.display = "block"
    // }

    // document.getElementById("edit_btn_account").style.display = "none"
    // document.getElementById("save_btn_account").style.display = "block"
    // document.getElementById("cancel_btn_account").style.display = "block"
}

function CancelEditsAccount() {
    user_vals = document.getElementsByClassName("user-val")
    field_inputs = document.getElementsByClassName("account-field-input")

    for (i = 0; i < user_vals.length; i++) {
        user_vals[i].style.display = "block"
        field_inputs[i].style.display = "none"
    }
    document.getElementById("edit_btn_account").style.display = "block"
    document.getElementById("save_btn_account").style.display = "none"
    document.getElementById("cancel_btn_account").style.display = "none"
}

function SaveEditsAccount() {
    form = document.getElementById("Account-details")
    form.submit()
}


// Privacy

function EnableEditPrivacy() {
    field_inputs = document.getElementsByClassName("privacy-field-input")

    for (field_input of field_inputs) {
        field_input.disabled = false
    }

    document.getElementById("edit_btn_privacy").style.display = "none"
    document.getElementById("save_btn_privacy").style.display = "block"
    document.getElementById("cancel_btn_privacy").style.display = "block"
}

function CancelEditsPrivacy() {
    // field_inputs = document.getElementsByClassName("privacy-field-input")
    
    // for(field_input of field_inputs){
    //     field_input.disabled = true
    // }

    // document.getElementById("edit_btn_privacy").style.display = "block"
    // document.getElementById("save_btn_privacy").style.display = "none"
    // document.getElementById("cancel_btn_privacy").style.display = "none"
    
}

function SaveEditsPrivacy() {
    form = document.getElementById("Privacy-details")
    form.submit()
}