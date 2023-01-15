# CS50 Web Programming Final Project (Capstone): E-planner

## Overview:
E-planner is a webpage designed to allow users to keep track of their events and organise their day seamlessly. The webpage will allow users to:
* Create events
* Invite other users to their events
* Accept or reject an event
* Organisers may delete an event
* A calender layout to keep track of all monthly events, and navigating the calender to other months

<hr />

## Distinctiveness and Complexity:
This project is sufficiently distinct from other projects in this course as a planner/ calender application has not been done before in any of the projects. It is also sufficiently distinct as it is not an e-commerce site nor a social network site.

The project is sufficiently complex as it contains more than one django model, and has various javascript functions for the front-end. The project also fulfills mulitple requirements for the application to work, as listed below:
1. **Home page**
	* Current users may login to have access to any of the application's functions.
	* New users may register and create a new account.
2. **Django models**
	* User model
	* Event model with the following fields: created by, title, description, date, start time, end time
	* UserEvent model with the following fields: User, Event, status (whether a user has accepted, declined, or not respond to an event invite)
3. **Creating new events**
	* Users who are signed in can fill in a form to create an event. The form has the following fields: event title, event description, date, start time, end time, and attendees. All form fields are required, except for event description and attendees. 
	* Users cannot create an event before today's date.
	* Users cannot create an event if the start time is later than or equal to the end time.
	* Users cannot create an event on an invalid date (e.g. 31 Feb)
	* Users cannot create an event if the attendees selected are unavailable.
	* Otherwise, if an event is successfully created, the page will let the user know that the event has been created.
4. **Invites page**
	* Users who created an event will automatically accept that event.
	* The page should show events which the user has been invited to. It will display the event title, description, date, start and end time.
	* Users should be able to accept / reject an event.
	* Users cannot accept an event, if they are unavailable.
5. **Monthly calender page**
	* User should be able to navigate the calender to the previous and next month.
	* All accepted event title should be displayed on the calender on their respective date.
	* Clicking on any of the dates on the calender will display event details (if any), such as event title, description, date, start and end time.
6. **Delete Event**
	* Users who created an event will have the function to delete the event.
	* Attendees who have accepted the event will no longer see the event displayed on their calender.
7. **Reject Event**
	* Attendees who have accepted the event can reject the event after accepting.
8. **Mobile responsive**
	* The webpage is responsive to screen of different sizes.

<hr />

## File information:
* The functions in **views.py** are:
	* Class NewEventForm: Django form for creating a new event
	* home: To render homepage
	* login_view, logout_view, register: To login, logout, or register users
	* create_event: Function to create a new event
	* invites: To retrieve all event which the user has been invited to, and render invites page
	* accept: To accept an event
	* decline: To decline an event
	* event: To retrieve all event information for today, and for the current month and year, and finally to render events page
	* get_event: To retrieve all event information for a particular day
	* delete_event: To delete an event
	* reject_event: To reject an event after accepting
* The models in **models.py** are:
	* User model
	* Event model
	* UserEvent model
* The functions in **index.js** are:
	* update_status: To accept/ reject an event on invites page
	* getAllDaysInMonth: To get all the days in that month and year
	* next: To display the calender for next month
	* previous: To display the calender for previous month
	* event_details: To display the event details after clicking on a date
* **styles.css** containing all css styling used
* Templates used for the different html pages (e.g. create_event.html, event.html, home_page.html, invites.html, layout.html, login.html, register.html)
* Other files such as urls.py, admin.py, ... etc

<hr />

## How to run the application:
1. Install python packages required to run the web application by running pip install -r requiremens.txt
2. Run python manage.py makemigrations planner to make migrations for the planner app.
3. Run python manage.py migrate to apply migrations to your database.

<hr />

## Video Demonstration
* https://youtu.be/dq_ELrKDEj0


