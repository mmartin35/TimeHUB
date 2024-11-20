# Pointing System

1. **[Introduction](#introduction)**  
   - [Overview of the Pointing System Project](#overview-of-the-pointing-system-project)  
   - [Key Features](#key-features)  

2. **[Project Overview](#project-overview)**  
   - [Calendar for Events](#calendar-for-events)  
   - [Event Submission](#event-submission)  
   - [Work Time Tracking](#work-time-tracking)  
   - [Admin Panel Features](#admin-panel-features)  
   - [Intern Management](#intern-management)  
   - [Dynamic Week Navigation](#dynamic-week-navigation)  

3. **[Technologies Used](#technologies-used)**  
   - [Frontend Technologies](#frontend-technologies)  
   - [Backend Technologies](#backend-technologies)  

4. **[Installation Instructions](#installation-instructions)**  
   - [Clone the Repository](#clone-the-repository)  
   - [Install Dependencies](#install-dependencies)  
   - [Set Up the Database](#set-up-the-database)  
   - [Development Setup](#development-setup)  
   - [Production Setup](#production-setup)  

5. **[Directory Structure](#directory-structure)**  

6. **[Models Overview](#models-overview)**  
   - [User Models](#user-models)  
   - [Planning Models](#planning-models)  
   - [Pointer Models](#pointer-models)  

7. **[Technical Information](#technical-information)**  
   - [Approbation Values](#approbation-values)  
   - [Authentication System](#authentication-system)  

8. **[Additional Information](#additional-information)**  
   - [Supervisor Details](#supervisor-details)  
   - [Project Timeline](#project-timeline)  
   - [Integration with DLH Internship Management System](#integration-with-dlh-internship-management-system)

## Introduction

### Project Overview

This project is a web-based planning and event management tool built using Django for the backend and FullCalendar and Bootstrap for the frontend. It allows users to submit day-off requests, view a calendar of events, and manage various aspects of their schedule. The project includes a stopwatch feature to track work times and functionality to manage interns and events through an admin panel.

### Key Features

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

### Frontend
- FullCalendar for calendar UI and event handling.
- jQuery for DOM manipulation.
- Bootstrap 5.0 for styling the calendar, including color-coding events and day numbers, and customizing month and day headers.
### Backend
- Web framework: Django
- Database: SQLite
- API calls: requests

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
### Development

Start the Django development server:

``` bash
python3 manage.py runserver
```
Open your browser and navigate to http://localhost:8000.

### Production

Go on the django_to_prod.md documentation to get more details.

## Directory Structure

``` bash
.
├── PS/
│   ├── asgi.py
│   ├── settings.py             # Django config
│   ├── urls.py                 # URL routing for the project
│   └── wsgi.py
├── my_app/
│   ├── templates/
│   │   └── my_app.html         # HTML template
│   ├── models.py               # Django models
│   ├── views.py                # Views
│   ├── static/
│   │   └── my_app/
│   │       └── css/
│   │           └── my_app.css  # Custom styles for the UI
│   └── urls.py                 # URL routing for the app
├── templates/
│   ├── base.html				        # Shared base template
│   └── navbar.html				      # Navbar depending on logged-in user
├── static/
│	├── images.png
│   └── css/
│       ├── base.css  			    # Custom styles for the base
│       └── navbar.css			    # Custom styles for the navbar
├── requirements.txt            # Python dependencies
└── manage.py                   # Django management script
```

## Models Overview

### user

- Member:
  Represents each staff user.<br>

  ``` python
  ├── user		# ForeignKey relationship with the User model
  └── email		# personal email address
  ```

- Intern:
  Represents each intern user.<br>

  ``` python
  ├── user			      # ForeignKey relationship with the User model
  ├── cns				      # CNS number
  ├── internship_type # (stage conventionné, stage pratique...)
  ├── department		  # (IT, HR...)
  ├── tutor
  ├── mission
  │
  ├── arrival			    # first day of internship
  ├── departure		    # last day of internship
  ├── is_ongoing		  # presence in the company
  ├── is_active		    # presence at office
  │
  ├── daysoff_total	  # days off total during the internship
  ├── daysoff_left	  # days off available
  ├── daysoff_onhold	# days off still to be processed
  │
  └── regime			    # percentage in reference to full time
  ```

### planning

- Event:

  Represents day-off or leave requests.<br>

  ``` python
  ├── intern			  # ForeignKey relationship with the Intern model
  ├── request_date
  │
  ├── reason
  ├── is_half_day
  ├── start_date
  ├── end_date
  ├── duration
  │
  ├── approbation		  # check technical informations for more details
  └── comment			    # comment from staff for approbation
  ```

- PublicHolidays:

  Represents vacations.<br>

  ``` python
  ├── name
  └── date
  ```

### pointer

- DailyTimer:

  Tracks work start and end times for both morning and afternoon sessions.<br>

  ``` python
  ├── intern		# ForeignKey relationship with the Intern model
  ├── date
  │
  ├── worktime	# sum of t1, t2 and t3, t4
  ├── t2			  # time of timer 2
  ├── t3			  # time of timer 3
  ├── t4			  # time of timer 4
  └── t1			  # time of timer 1
  ```

- ServiceTimer:

  Tracks out of office times.<br>

  ``` python
  ├── intern		# ForeignKey relationship with the Intern model
  ├── date
  ├── comment		# comment from staff for approbation
  │
  ├── t1			  # time of timer 1
  └── t2			  # time of timer 2
  ```

- RequestTimer:

  Represents timer correction requests.<br>

  ``` python
  ├── intern		  # ForeignKey relationship with the Intern model
  ├── date
  ├── approbation	# check technical informations for more details
  ├── comment		  # comment from staff for approbation
  │
  ├── original_t1	# save of timer 1
  ├── original_t2	# save of timer 1
  ├── original_t3	# save of timer 1
  ├── original_t4	# save of timer 1
  │
  ├── altered_t1	# changes for timer 1
  ├── altered_t2	# changes for timer 2
  ├── altered_t3	# changes for timer 3
  └── altered_t4	# changes for timer 4
  ```

- ChangingLog:
  Keeps database alterations.<br>

  ``` python
  ├── intern				    # ForeignKey relationship with the Intern model
  ├── member				    # username of staff username
  ├── date
  │
  ├── original_worktime	# save of worktime
  └── altered_worktime	# changes for worktime
  ```

## Technical information

### Approbation

 Integer field that can have the following values:

> 0: Pending<br>
> 1: Approved<br>
> 2: Rejected<br>
> 3: Cancelled<br>

### Authentication

The authentication system is based on OAuth2.0. The user is redirected to the login page of the company's website. Once the user is authenticated, the user is redirected to the pointing system.<br>
If you want to use or test the app, you will need to update the authentication system in the pointer app and use the Django built-in authentication system.<br>

## Additional Information

Supervisor: Chakib Senhadji<br>
Project start date: 09-02-2024<br>
Project duration: 2 months<br>
This project is part of the DLH internship management system.<br>
