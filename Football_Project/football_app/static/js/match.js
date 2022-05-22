
function addErrors (error) {
    const bodyModal = document.querySelector('.modal-body-style');
    if (bodyModal.children.length > 2){
        bodyModal.removeChild(bodyModal.lastElementChild);
    }
    const pElement = document.createElement('p');
    pElement.classList.add('error-style');
    pElement.innerText = error;
    const divElement = document.createElement('div');
    divElement.classList.add('row');
    divElement.appendChild(pElement.cloneNode(true));
    bodyModal.appendChild(divElement.cloneNode(true));
};


document.addEventListener("DOMContentLoaded", function () {
    
    for (let i=0, clickEl, clicksEl = document.querySelectorAll('[data-toggle="modal"]'); clickEl = clicksEl[i]; i++){
        clickEl.onclick = function (e) {
            e.preventDefault();
            const bodyModal = document.querySelector('.modal-body-style');
            if (bodyModal.children.length > 2){
                bodyModal.removeChild(bodyModal.lastElementChild);
            }
            bodyModal.firstElementChild.firstElementChild.innerText = e.target.dataset.team_home;
            bodyModal.firstElementChild.lastElementChild.innerText = e.target.dataset.team_away;
            bodyModal.lastElementChild.firstElementChild.firstElementChild.value = "";
            bodyModal.lastElementChild.lastElementChild.firstElementChild.value = "";
            
            document.querySelector('form').addEventListener('submit', function(event){
                event.preventDefault();
                const formField = event.target.elements;
                const obj = {
                    pk: e.target.dataset.id,
                    team_home_goals: formField[0].value,
                    team_away_goals: formField[1].value,
                };
                const urlPost = window.location.origin + e.target.dataset.url;
                fetch(urlPost, {
                    method: 'POST',
                    body: JSON.stringify(obj),
                })
                .then(response => {
                    if (response.status === 200){
                        return response.json();
                    }
                    else {
                        throw Error();
                    };
                })
                .then(data => {
                    if (data['status'] === 'True') {
                        window.location = window.location.href;
                    }
                    else if (data['status'] === 'False'){
                        addErrors('Błąd zapisu do bazy');
                    };
                })
                .catch(error => {
                    addErrors('Błąd połączenia z serwerem');
                });
            });
        }
    }
});
