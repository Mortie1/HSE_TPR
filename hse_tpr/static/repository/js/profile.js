let input = document.querySelector('input[name="q"]');
    
let answerField = document.getElementById("flex");

let t = 'cases_list';

async function loadDoc() {
    try {
    const response = await fetch(`/search_user/${t}?q=${input.value}`);
    if (response.status == 200) {
        const data = await response.json();
        let list = data.html;
        answerField.innerHTML= list;
        let hrefs = answerField.getElementsByTagName("a");
        for (var i = 0; i < hrefs.length; ++i) {
            hrefs[i].href = "../repository/case_update/" + hrefs[i].dataset.casePk + '/';
        }
    } else {
        console.error('Ошибка загрузки данных!');
    }
    } catch (error) {
    console.error(error);
    }
}

input.oninput = loadDoc;

loadDoc();

window.addEventListener('click', ({ target }) => {
    if (target.id === 'tiles') {
        t = 'cases_tiles';
        loadDoc();
    } else if (target.id === 'list') {
        t = 'cases_list';
        loadDoc();
    }
})