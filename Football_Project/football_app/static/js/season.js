function nextStep (formElement) {
    formElement.firstElementChild.classList.remove('display-active');
    formElement.firstElementChild.classList.add('display-none');
    formElement.lastElementChild.classList.remove('display-none');
    formElement.lastElementChild.classList.add('display-active');
};

{/* <p id="error_1_id_teams_played" class="invalid-feedback"><strong>Liczba drużyn musi być parzysta, min 10, max 24 drużyn</strong></p>
is-invalid */}

document.addEventListener("DOMContentLoaded", function() {

    const formElement = document.querySelector('form');

    document.querySelector('.next-step').addEventListener('click', function(event){
        const obj = {
            step: 1,
            league: formElement[0].value,
            date_start: formElement[1].value,
            teams_played: formElement[2].value,
        };
        const urlPost = window.location.href;
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
                nextStep(formElement);
            }
            else if (data['status'] === 'False'){
                // addErrors('Błąd zapisu do bazy');
            };
        })
        .catch(error => {
            // addErrors('Błąd połączenia z serwerem');
        });
    });
    document.querySelector('.prev-step').addEventListener('click', function(event){
        formElement.firstElementChild.classList.remove('display-none');
        formElement.firstElementChild.classList.add('display-active');
        formElement.lastElementChild.classList.remove('display-active');
        formElement.lastElementChild.classList.add('display-none');
    });
});