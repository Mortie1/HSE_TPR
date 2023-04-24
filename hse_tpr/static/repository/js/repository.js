let input = document.querySelector('input[name="q"]');
    
let answerField = document.getElementById("flex");

let t = 'cases_tiles';

async function loadDoc() {
    try {
    const response = await fetch(`/search/${t}?q=${input.value}`);
    if (response.status == 200) {
        const data = await response.json();
        let list = data.html;
        answerField.innerHTML= list;
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