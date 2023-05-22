let common_inputs = document.querySelectorAll(".form-control");
let select_inputs = document.querySelectorAll(".form-select");

for (var i = 0; i < common_inputs.length; ++i) {
    common_inputs[i].disabled = true;
    common_inputs[i].placeholder = '';
}

for (var i = 0; i < select_inputs.length; ++i) {
    let options = select_inputs[i].getElementsByTagName("option");
    let selected_options = []
    for (var j = 0; j < options.length; ++j) {
        if (options[j].selected === true) {
            options[j].selected = false;
            selected_options.push(options[j]);
        }
    }
    select_inputs[i].innerHTML = '';
    for (var j = 0; j < selected_options.length; ++j) {
        
        select_inputs[i].appendChild(selected_options[j]);
    }
    select_inputs[i].disabled = true;
    select_inputs[i].placeholder = '';
}