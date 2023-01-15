document.addEventListener('DOMContentLoaded', function() {
    // loop
    document.querySelectorAll('.edit_post').forEach(button => {
        button.addEventListener('click', () => edit_post(button.dataset.id));
    })

    document.querySelectorAll('.heart').forEach(heart => {
        heart.addEventListener('click', () => like_post(heart.dataset.id, heart.dataset.like));
    })
})


function edit_post(post_id) {
    let element = document.createElement('textarea');
    element.rows = '3';
    element.cols = '245';
    element.id = `post_textarea_${post_id}`
    element.innerHTML = document.getElementById(`post_content_${post_id}`).innerText;

    document.querySelector(`#post_content_${post_id}`).style.display = 'none';
    document.querySelector(`#post_content_div_${post_id}`).append(element);

    // Change edit button to save button
    let save_button = document.createElement('button');
    save_button.innerHTML = 'Save';
    save_button.className = 'btn btn-primary';
    save_button.id = `save_post_${post_id}`
    save_button.style ='float: right';
    // Onclick, addEventListener
    save_button.addEventListener('click', function() {
        // Get textarea element
        const new_post = document.getElementById(`post_textarea_${post_id}`).value;

        // Save to database
        fetch(`/edit_post/${post_id}`, {
            method: 'POST',
            body: JSON.stringify({'new_post': new_post})
        })
        .then(function(response) {
            // Restore post
            document.querySelector(`#post_textarea_${post_id}`).style.display = 'none';
            let post_content = document.querySelector(`#post_content_${post_id}`);
            post_content.innerHTML = new_post;
            post_content.style.display = 'block';

            // Restore edit button
            document.querySelector(`#edit_post_${post_id}`).style.display = 'block';
            document.querySelector(`#save_post_${post_id}`).style.display = 'none';
        })
    })

    document.querySelector(`#edit_post_${post_id}`).style.display = 'none';
    document.querySelector(`#post_${post_id}`).append(save_button);
}


function like_post(post_id, like) {
    if (like === "like") {
        fetch(`/like/${post_id}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(count => {
            // change heart icon
            document.querySelector(`#like_${post_id}`).style.display = 'none';
            document.querySelector(`#unlike_${post_id}`).style.display = 'inline';

            // update like count
            document.querySelector(`#like_count_${post_id}`).innerHTML = `${count['count']} likes`;
        })
    }
    else {
        fetch(`/unlike/${post_id}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(count => {
            // change heart icon
            document.querySelector(`#like_${post_id}`).style.display = 'inline';
            document.querySelector(`#unlike_${post_id}`).style.display = 'none';

            // update like count
            document.querySelector(`#like_count_${post_id}`).innerHTML = `${count['count']} likes`;            
        })
    }
}