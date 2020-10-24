const BASE_URL = 'http://localhost:8000/api/v1/';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

async function makeRequest(url, method='GET', data=undefined) {
    let opts = {method, headers: {}};
    if (!csrfSafeMethod(method))
        opts.headers['X-CSRFToken'] = getCookie('csrftoken');
    if (data) {
        opts.headers['Content-Type'] = 'application/json';
        opts.body = JSON.stringify(data);
    }
    let response = await fetch(url, opts);
    if (response.ok) {  // нормальный ответ
        return response.json();
    } else {            // ошибка
        let error = new Error(response.statusText);
        error.response = response;
        throw error;
    }
}

async function favorites(event) {
    event.preventDefault();
    let likeBtn = event.target;
    let url = likeBtn.href;

    try {
        let response = await makeRequest(url, 'POST');
        console.log(response);

    }
    catch (error) {
        console.log(error);
    }

    likeBtn.classList.add('hidden');
    const unlikeBtn = likeBtn.parentElement.getElementsByClassName('unlike')[0];
    unlikeBtn.classList.remove('hidden');
}

async function unfavorites(event) {
    event.preventDefault();
    let unlikeBtn = event.target;
    let url = unlikeBtn.href;

    try {
        let response = await makeRequest(url, 'DELETE');
        console.log(response);
    }
    catch (error) {
        console.log(error);
    }

    unlikeBtn.classList.add('hidden');
    const likeBtn = unlikeBtn.parentElement.getElementsByClassName('like')[0];
    likeBtn.classList.remove('hidden');
}

window.addEventListener('load', function() {
    const likeButtons = document.getElementsByClassName('like');
    const unlikeButtons = document.getElementsByClassName('unlike');

    for (let btn of likeButtons) {btn.onclick = favorites}
    for (let btn of unlikeButtons) {btn.onclick = unfavorites}
});
