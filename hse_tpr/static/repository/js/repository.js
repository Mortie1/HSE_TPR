let input = document.querySelector('input[name="q"]');

let filters = {
    'Platform': 'None',
    'information_author_name': ''
};

function parseFilters() {
    result = '';
    for (const [key, value] of Object.entries(filters)) {
        result += `&${key}=${value}`;
    }
    return result;
}


let answerField = document.getElementById("flex");

let t = 'cases_list';

async function loadDoc() {
    try {
    const response = await fetch(`/search/${t}?q=${input.value}` + parseFilters());
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

document.getElementById('submit-filters').addEventListener("click", () => {
    for (const [filter, val] of Object.entries(filters)) {
        filters[filter] = document.getElementById(filter).value;
    }
    loadDoc();
})
