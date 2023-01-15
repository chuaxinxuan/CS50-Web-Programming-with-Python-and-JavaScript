document.addEventListener('DOMContentLoaded', function() {
    // loop
    document.querySelectorAll('.invite_button').forEach(button => {
        button.addEventListener('click', (event) => update_status(event, button.dataset.id))
    })

    document.querySelector('#next_button').addEventListener('click', () => next());
    document.querySelector('#prev_button').addEventListener('click', () => prev());

    document.querySelectorAll('table.calender_table td').forEach(data_table => {
        data_table.addEventListener('mouseover', function(event) {
            let element = event.target;
            
            if (element.innerText != "") {
                element.style = 'cursor: pointer';
            }
        })
    })

    document.querySelectorAll('table.calender_table td').forEach(data_table => {
        data_table.addEventListener('click', () => event_details(data_table.dataset.id));
    })
})


function update_status(event, event_id) {
    let element = event.target

    // accept or decline
    if (element.innerHTML === 'Accept') {
        fetch(`/accept/${event_id}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(status => {
            if (status['status'] === 'fail') {
                document.querySelector('.alert').style.display = 'block';
            }
            else {
                // animation
                element.parentElement.parentElement.style.animationPlayState = 'running';
                element.parentElement.parentElement.addEventListener('animationend', () => {
                    element.parentElement.parentElement.remove();
                });
            }
        }) 
    }
    else {
        fetch(`/decline/${event_id}`, {
            method: 'POST'
        })
        .then(function(response) {
            // animation
            element.parentElement.parentElement.style.animationPlayState = 'running';
            element.parentElement.parentElement.addEventListener('animationend', () => {
                element.parentElement.parentElement.remove();
            });
        })
    }
}


function getAllDaysInMonth(year, month) {
    const all_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                        'August', 'September', 'October', 'November', 'December'];

    const date = new Date(year, all_months.indexOf(month), 1);
    const dates = [];

    while (date.getMonth() === all_months.indexOf(month)) {
        dates.push(new Date(date).getDate());
        date.setDate(date.getDate() + 1);
    }
    return dates;
}


function next() {
    const all_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                        'August', 'September', 'October', 'November', 'December'];

    const month_year = document.getElementById('month_year').innerText;
    const split = month_year.split(' ');
    let month = split[0];
    let year = parseInt(split[1]);

    // increase month_year by 1
    let index = all_months.indexOf(month);
    index = (index+1) % 12;
    if (index === 0) {
        year = year + 1;
    }
    document.querySelector('#month_year').innerHTML = `${all_months[index]} ${year}`;


    // update dates in calender
    const weekMap = {1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 0:6};
    new_dates = getAllDaysInMonth(year, all_months[index]);
    new_dates = Array(weekMap[new Date(year, index, 1).getDay()]).fill('').concat(new_dates); 
    new_dates = new_dates.concat(Array(42 - new_dates.length).fill(''));
    // update innerhtml of td
    document.querySelectorAll('table.calender_table td').forEach(grid => {
        let i = parseInt(grid.dataset.id)-1;
        if (new_dates[i] !== "") {
            // fetch event
            fetch(`/get_event/${year}/${index+1}/${new_dates[i]}`)
            .then(response => response.json())
            .then(event => {
                let temp_innerhtml = `${new_dates[i]}`;
                for (e in event.event_title) {
                    temp_innerhtml = temp_innerhtml + `<div class="event_summary">${event.event_title[e]}</div>`
                }
                grid.innerHTML = temp_innerhtml;
            })
        }
        else {
            grid.innerHTML = `${new_dates[i]}`;
        }
    })        
}


function prev() {
    const all_months = ['December', 'November', 'October', 'September', 'August', 'July',
                        'June', 'May', 'April', 'March', 'February', 'January'];

    const month_year = document.getElementById('month_year').innerText;
    const split = month_year.split(' ');
    let month = split[0];
    let year = parseInt(split[1]);

    // decrease month_year by 1
    let index = all_months.indexOf(month);
    index = Math.abs(index+1) % 12;
    if (index === 0) {
        year = year - 1;
    }
    document.querySelector('#month_year').innerHTML = `${all_months[index]} ${year}`;


    // update dates in calender
    const weekMap = {1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 0:6};
    const monthMap = {0:11, 1:10, 2:9, 3:8, 4:7, 5:6, 6:5, 7:4, 8:3, 9:2, 10:1, 11:0};
    new_dates = getAllDaysInMonth(year, all_months[index]);
    new_dates = Array(weekMap[new Date(year, monthMap[index], 1).getDay()]).fill('').concat(new_dates); 
    new_dates = new_dates.concat(Array(42 - new_dates.length).fill(''));
    // update innerhtml of td
    document.querySelectorAll('table.calender_table td').forEach(grid => {
        let i = parseInt(grid.dataset.id)-1;
        if (new_dates[i] !== "") {
            // fetch event
            fetch(`/get_event/${year}/${monthMap[index]+1}/${new_dates[i]}`)
            .then(response => response.json())
            .then(event => {
                let temp_innerhtml = `${new_dates[i]}`;
                for (e in event.event_title) {
                    temp_innerhtml = temp_innerhtml + `<div class="event_summary">${event.event_title[e]}</div>`
                }
                grid.innerHTML = temp_innerhtml;
            })
        }
        else {
            grid.innerHTML = `${new_dates[i]}`;
        }
    })        
}


function event_details(data_id) {
    // get date
    const weekMap = {1:0, 2:1, 3:2, 4:3, 5:4, 6:5, 0:6};
    const all_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                        'August', 'September', 'October', 'November', 'December'];

    const month_year = document.querySelector('#month_year').innerText;
    const month = month_year.split(' ')[0];
    const year = month_year.split(' ')[1];
    new_dates = getAllDaysInMonth(year, month);
    new_dates = Array(weekMap[new Date(year, all_months.indexOf(month), 1).getDay()]).fill('').concat(new_dates); 
    new_dates = new_dates.concat(Array(42 - new_dates.length).fill(''));
    const day = new_dates[data_id - 1];

    if (day != "") {
        // update date
        document.querySelector('#event_details_date').innerHTML = `${day} ${month_year} Events:`;

        // update event
        // fetch event
        fetch(`/get_event/${year}/${all_months.indexOf(month)+1}/${day}`)
        .then(response => response.json())
        .then(event => {
            // if there are no events:
            if (event.event_title.length == 0) {
                document.querySelector('#event_details').innerHTML = 'There are no events.';
            }
            else {
                // clear innerhtml
                document.querySelector('#event_details').innerHTML = '';
                for (let e=0; e < event.event_title.length; e++) {
                    // create division element  
                    let element = document.createElement('div');
                    element.style = 'background-color:lavender; padding: 5px; margin: 5px; border-radius: 5px; border: 1px solid darkviolet;'
                    element.innerHTML = `<h5>${event.event_title[e]}</h5>
                                <ul>
                                    <li>Organiser: ${event.event_organiser[e]}</li>
                                    <li>Time: ${event.event_starttime[e]} to ${event.event_endtime[e]}</li>
                                    <li>Description: ${event.event_description[e]}</li>
                                </ul>`;

                    // check if event_organiser is user
                    if (event.request_user == event.event_organiser[e]) {
                        let delete_link = document.createElement('a');
                        delete_link.style = 'margin-left: 5px';
                        delete_link.innerHTML = 'Delete';
                        delete_link.className = 'btn btn-dark';
                        delete_link.setAttribute('role', 'button');
                        delete_link.setAttribute('href', `../delete_event/${event.event_id[e]}`);
                        element.appendChild(delete_link);
                    }
                    else {
                        console.log('hii');
                        let reject_link = document.createElement('a');
                        reject_link.style = 'margin-left: 5px';
                        reject_link.innerHTML = 'Reject';
                        reject_link.className = 'btn btn-danger';
                        reject_link.setAttribute('role', 'button');
                        reject_link.setAttribute('href', `../reject_event/${event.event_id[e]}`);
                        element.appendChild(reject_link);
                    }
                    document.querySelector('#event_details').append(element);
                }
            }
        })
    }
}