document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send mail
  document.querySelector('#compose-form').addEventListener('submit', send_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function load_email(email_id, mailbox) {
  // Mark email as read
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })

  // Hide header content and mailbox content:
  document.querySelector('#mailbox_header').style.display = 'none';
  document.querySelectorAll('.emails-list').forEach(function(ele) {
    ele.style.display = 'none';
  });

  // Get email contents:
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    // then show the below contents:
    console.log(email['body']);
    let element = document.createElement('div');
    element.innerHTML = `<h6 style='display: inline;'>From:</h6> ${email['sender']} <br>
                         <h6 style='display: inline;'>To:</h6> ${email['recipients']} <br>
                         <h6 style='display: inline;'>Subject:</h6> ${email['subject']} <br>
                         <h6 style='display: inline;'>Timestamp:</h6> ${email['timestamp']} <br><br>
                         <div style='display: block;'>${email['body'].replace(/\n/g, "<br />")}</div> <br><br>`
    // Append
    document.querySelector('#emails-view').append(element);


    // Archive & Unarchive
    if (mailbox !== 'sent') {
      let archive_button = document.createElement('button');
      if (email['archived'] === false) {
        archive_button.className = 'btn btn-sm btn-outline-primary';
        archive_button.innerHTML = 'Archive';
        // Onclick, archive email
        archive_button.addEventListener('click', function() {
          fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: true
            })
          })
          .then(response => load_mailbox('inbox'));
        })
      }
      else {
        archive_button.className = 'btn btn-sm btn-outline-primary';
        archive_button.innerHTML = 'Unarchive';
        // Onclick, unarchive email
        archive_button.addEventListener('click', function() {
          fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: false
            })
          })
          .then(response => load_mailbox('inbox'));
        })
      }
      // Append
      document.querySelector('#emails-view').append(archive_button);
    }


    // Reply
    let reply_button = document.createElement('button');
    reply_button.className = 'btn btn-sm btn-outline-primary';
    reply_button.innerHTML = 'Reply';
    if (mailbox !== 'sent') {
      reply_button.style.marginLeft = '5px';
    }
    // Onclick event
    reply_button.addEventListener('click', function() {
      // Show the compose-view and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';  
      // Prefill form
      document.querySelector('#compose-recipients').value = email['sender'];
      if (email['subject'].slice(0,3) === 'Re:') {
        document.querySelector('#compose-subject').value = email['subject'];
      }
      else {
        document.querySelector('#compose-subject').value = 'Re: ' + email['subject'];
      }
      let dotted_line = '-';
      document.querySelector('#compose-body').value = `\n${dotted_line.repeat(70)}\nOn ${email['timestamp']} ${email['sender']} wrote: \n${email['body']}`;
    })
    // Append
    document.querySelector('#emails-view').append(reply_button);
  })
}


function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3 id='mailbox_header'>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Send a GET request to the URL
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Loop through the json
    emails.forEach(function(email) {
      // Create a new division
      let element = document.createElement('div');
      element.classList.add("emails-list");
      element.style.width = '1110px';
      element.style.height = '40px';
      element.style.border = '1px solid #DCDCDC';
      element.style.paddingLeft = '5px';
      element.style.paddingTop = '6px';
      element.style.paddingRight = '6px';

      if (email['read'] === true) {
        element.style.backgroundColor = '#F0F0F0';
      }

      element.innerHTML = `<h6 style='display: inline; padding-right: 5px;'>${email['sender']}</h6> ${email['subject']}
                          <p style='display: inline-block; float: right;'>${email['timestamp']}</p>`;

      // When mouseover, shadow appears on div
      element.addEventListener('mouseover', function() {
        element.style.backgroundColor = '#D8D8D8';
      })
      // When mouse leave, shadow disappears on div
      element.addEventListener('mouseleave', function() {
        if (email['read'] === true) {
          element.style.backgroundColor = '#F0F0F0';
        }
        else {
          element.style.backgroundColor = 'white';
        }
      })

      // Onclick, show the email contents
      element.addEventListener('click', () => load_email(email['id'], mailbox));

      // Append
      document.querySelector('#emails-view').append(element);
    })
  })
}


function send_mail(event) {
  event.preventDefault();
  // Get form values
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // POST emails
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    })
  })
  .then(response => response.json())
  .then(result => {
    // If email is unsuccessful, send alert
    if (result.error !== undefined) {
      alert(result.error);
    }
    else {
    // Load sent mailbox
    load_mailbox('sent');
    }
  });
  // Stop form from submitting
  return false;
}