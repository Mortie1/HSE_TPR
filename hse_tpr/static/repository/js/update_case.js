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

const exampleModal = document.getElementById('modal-add-my-variant')

if (exampleModal) {
    exampleModal.addEventListener('show.bs.modal', event => {
        console.log('initiated');

        // Button that triggered the modal
        const button = event.relatedTarget;

        // Extract info from data-bs-* attributes
        const field = button.getAttribute('data-bs-field-id');
        const modalBodyInput = document.getElementById('input-my-variant');

        // remove event listeners
        var el = document.getElementById('submit-my-variant'),
        elClone = el.cloneNode(true);
        el.parentNode.replaceChild(elClone, el);
        
        // If necessary, you could initiate an Ajax request here
        // and then do the updating in a callback.
        document.getElementById('submit-my-variant').addEventListener("click", () => {
            console.log('initiated post request');
            const xhr = new XMLHttpRequest();
            xhr.open('POST', "../../../add_my_variant/");
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
            console.log(field.split("id_")[1]);
            xhr.send(JSON.stringify({
                "field": field.split("id_")[1],
                "input": modalBodyInput.value
            }));
            xhr.onload = () => {
                if (xhr.status !== 200) {
                    modalBodyInput.classList.add('invalid');
                    console.log("ERROR. STATUS NOT 200");
                } else {
                    const parsed = JSON.parse(xhr.response);
                    const id = parsed['id'];
                    var opt = document.createElement('option');
                    opt.value = id;
                    opt.innerHTML = modalBodyInput.value;
                    document.getElementById(field).appendChild(opt);
                    if (field === 'id_case_department') {
                        var opt1 = document.createElement('option');
                        opt1.value = id;
                        opt1.innerHTML = modalBodyInput.value;
                        document.getElementById('id_information_author_department').appendChild(opt1);
                    } else if (field === 'id_information_author_department') {
                        var opt1 = document.createElement('option');
                        opt1.value = id;
                        opt1.innerHTML = modalBodyInput.value;
                        document.getElementById('id_case_department').appendChild(opt1);
                    }
                }
                exampleModal.querySelector(".btn-secondary").click();
            };
        })
        // Update the modal's content.
    })
    
}