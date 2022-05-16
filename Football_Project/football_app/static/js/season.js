
document.addEventListener("DOMContentLoaded", function () {
    var numberOfTeams = 0;
    const labelElement = document.querySelectorAll('label');
    const checkboxElement = document.querySelectorAll('input[type=checkbox]');
    
    for (let i=0; i<checkboxElement.length;  i++){
        if (checkboxElement[i].checked){
            numberOfTeams += 1;
        }
        if (numberOfTeams > 0){
            labelElement[2].innerText = 'Drużyny, zaznaczonych ' + String(numberOfTeams) + '*';
        }
    }
    
    for (let i=0, checkboxEl, checkboxsEl = document.querySelectorAll('input[type=checkbox]'); checkboxEl = checkboxsEl[i]; i++){
        checkboxEl.onchange = function (e) {
            if (this.checked){
                numberOfTeams +=  1;
                labelElement[2].innerText = 'Drużyny, zaznaczonych ' + String(numberOfTeams) + '*';
            }
            else {
                numberOfTeams -= 1;
                if (numberOfTeams == 0){
                    labelElement[2].innerText = 'Drużyny*';
                }
                else {
                    labelElement[2].innerText = 'Drużyny, zaznaczonych ' + String(numberOfTeams) + '*';
                }
            }
        }
    }
});
