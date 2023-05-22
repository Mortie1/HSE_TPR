let names_button = document.getElementById("names_button");
let names_form = document.getElementById("first_name_and_last_name");
let passwords_form = document.getElementById("password");
let passwords_button = document.getElementById("passwords_button");

function getCookie(name) {
    if (!document.cookie) {
      	return null;
    }
  
    const xsrfCookies = document.cookie.split(';')
	.map(c => c.trim())
	.filter(c => c.startsWith(name + '='));
    if (xsrfCookies.length === 0) {
      	return null;
    }
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}

const csrftoken = getCookie('csrftoken');

function send_post(url, body, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', url);
    xhr.setRequestHeader('X-CSRFToken', csrftoken);
    xhr.send(JSON.stringify(body));
	xhr.onload = () => {
        callback(xhr.response);
    };
}

names_button.addEventListener("click", () => {
    if (names_button.value === '0') {
        var inputs = names_form.querySelectorAll(".form-control");
        for (var i = 0; i < inputs.length; ++i) {
            inputs[i].disabled = false;
        }
        names_button.value = '1';
        names_button.innerText = 'Сохранить';
    } else if (names_button.value === '1') {
        var inputs = names_form.querySelectorAll(".form-control");
        for (var i = 0; i < inputs.length; ++i) {
            inputs[i].disabled = true;
        }
        names_button.value = '0';
        names_button.innerText = 'Изменить';
        var body = {
            "first_name": document.getElementById("first_name_field").value,
            "last_name": document.getElementById("last_name_field").value
        };
        send_post('save_name/', body, () => {})
    }
})


passwords_button.addEventListener("click", () => {

    if (passwords_button.value === '0') {
        var inputs = passwords_form.querySelectorAll(".form-control");
        for (var i = 0; i < inputs.length; ++i) {
            inputs[i].disabled = false;
            inputs[i].style.display = "block";
        }
        passwords_button.value = '1';
        passwords_button.innerText = 'Сохранить';
    } else if (passwords_button.value === '1') {
        var inputs = passwords_form.querySelectorAll(".form-control");
        var body = {
            "first_password": document.getElementById("first_password_field").value,
            "second_password": document.getElementById("second_password_field").value
        };
        for (var i = 0; i < inputs.length; ++i) {
            inputs[i].disabled = true;
            inputs[i].value = '';
        }
        inputs[1].style.display = 'none';
        passwords_button.value = '0';
        passwords_button.innerText = 'Изменить';
        
        send_post('save_password/', body, (response) => {
            var parsed = JSON.parse(response);
            document.querySelector(".password_errors").innerHTML = parsed['html'];
        })
    }
})