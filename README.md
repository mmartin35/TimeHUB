# Pointing System

## Table of Contents

Links:<br>
https://trello.com/w/dlhpointingsystem<br>

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Installation Instructions](#installation-instructions)
- [Directory Structure](#directory-structure)
- [Models Overview](#models-overview)
- [Future Enhancements](#future-enhancements)
- [Troubleshooting](#troubleshooting)
- [Additional Information](#additional-information)
- [Contact Information](#contact-information)

## Project Overview

This project is a web-based planning and event management tool built using Django for the backend and FullCalendar and Bootstrap for the frontend. It allows users to submit day-off requests, view a calendar of events, and manage various aspects of their schedule. The project includes a stopwatch feature to track work times and functionality to manage interns and events through an admin panel.
Key Features

1. Calendar for Events
Displays a monthly view using FullCalendar.<br>
Allows users to submit events on specific dates or day-off requests.<br>
Dynamically loads events via AJAX from a Django URL endpoint (events_json).<br>
Color-codes events based on approval status (e.g., approved events in red, pending events in blue).<br>
The calendar has fixed dimensions to prevent resizing when switching between months.<br>

2. Event Submission
Users can submit day-off requests via a form on the right side of the calendar.<br>
The form captures:
- Event date (auto-filled when a date is clicked on the calendar).
- Reason for the request (e.g., "Sick," "Day-off").
- Start and end date for the absence.
- Half-day options to specify the exact time of leave and return.
Once submitted, the event is either pending approval or automatically handled depending on business logic.<br>

3. Work Time Tracking
Users can log work and lunch times using a server-side stopwatch feature.<br>
Buttons allow users to start/stop the work or lunch timer.<br>
Times are saved and managed via a Timer model that tracks both morning and afternoon work sessions.<br>

4. Admin Panel
The admin panel allows administrators to manage interns and events.<br>
Admins can approve or deny events, view intern details, and manage time-tracking data.<br>

5. Intern Management
Interns are managed within the Django admin panel and have relationships with timers and events.<br>
Work times are tracked via a Timer model, and each intern's work times are displayed in a carousel view for the current week.<br>

6. Dynamic Week Navigation
A carousel feature enables users to view timers and events for the current week, with the ability to navigate to past weeks.<br>

## Technologies Used

### Frontend:
- FullCalendar for calendar UI and event handling.
- jQuery for DOM manipulation.
- Bootstrap 5.0 for styling the calendar, including color-coding events and day numbers, and customizing month and day headers.
### Backend:
- Django as the web framework.
- A SQLite database for storing user, event, and timer data.
### Models:
- A User model for user authentication.
- An Intern model to manage user-related work information.
- A Timer model for worktime tracking.
- A Service model for service tracking.
- A Request model for managing timer changes.
- An Event model to manage user requests

## Installation Instructions
Clone the Repository:
``` bash
git clone git@github.com:mmartin35/pointing_system.git
cd pointing_system
```
Install Dependencies: Make sure to have Python and Django installed. Install required dependencies using:
``` bash
pip install -r requirements.txt
```
Set Up the Database: Apply migrations to set up the database schema:
``` bash
python3 manage.py makemigrations
python3 manage.py migrate
```
Run the Development Server: Start the Django development server:
``` bash
python3 manage.py runserver
```
Access the Application: Open your browser and navigate to http://localhost:8000.

## Directory Structure

``` bash
.
├── my_app/
│   ├── templates/
│   │   └── my_app.html   # Base template for the app
│   ├── models.py         # Django models (Timer, Intern, Events)
│   ├── views.py          # Views for handling events, timers, etc.
│   ├── static/
│   │   └── planning/
│   │       └── css/
│   │           └── planning.css  # Custom styles for FullCalendar and the UI
│   └── urls.py           # URL routing for the app
├── requirements.txt      # Python dependencies
└── manage.py             # Django management script
```

## Models Overview

- Intern:
  Represents each intern user.<br>
  Related to Timer and event models for tracking work time and day-off requests.<br>
- Timer:
  Tracks work start and end times for both morning and afternoon sessions.<br>
  ForeignKey relationship with the Intern model.<br>
- Event:
  Represents day-off or leave requests.<br>
  Includes fields like start_date, end_date, reason, and approval status.<br>

## Technical information

Approval status is an integer field that can have the following values:
> 0: Pending
> 1: Approved
> 2: Denied
> 3: Cancelled

Views only contains redirection pages. All the logic is in the handlers and the calc pages in PS.<br>

The authentication system is based on OAuth2.0. The user is redirected to the login page of the company's website. Once the user is authenticated, the user is redirected to the pointing system.<br>
If you want to use or test the app, you will need to update the authentication system in the pointer app and use the Django built-in authentication system.<br>

## Additional Information

Supervisor: Chakib Senhadji<br>
Project start date: 09-02-2024<br>
Project duration: 2 months<br>
This project is part of the DLH internship management system.<br>
