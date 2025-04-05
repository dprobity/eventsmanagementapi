# Overview

Event Management API
An Event Management System built with Django and Django REST Framework, allowing users to:

Create, manage, and explore events (with categories, capacity, ticket codes, only Organizers can create and update and manage events created by them.)

Register for events (including multiple tickets in one go)

Leave feedback on past events

Receive notifications (in-app)

Authenticate via JWT (JSON Web Tokens)


# Project Overview

- Features

- Tech Stack

- Local Setup

- Environment Variables (optional but recommended)

- Running Migrations & Server

- API Documentation – endpoints for each core resource

- Sample Requests & Responses

- Deployment Notes (brief)


Authentication & Users

Categories

Events

Registrations

Feedbacks

Notifications

Sample Requests & Responses

Deployment Notes

License

Project Overview
This API was created as part of an ALX Capstone Project to demonstrate a production-grade backend architecture. It follows RESTful principles, uses JWT authentication, and organizes logic into modular Django apps.

Features
User Management

Custom user model with is_organizer flag

JWT-based auth (/auth/login/, /auth/token/refresh/)

Categories

Separate app for event classification

Events

CRUD for events

Enforce capacity & show “selling out soon” logic

Filter & search by title, location, category, date range

Registrations

Multi-ticket purchase (quantity)

Auto-generated unique ticket codes for each seat

Waitlist logic if event is full

Feedbacks

Comments & ratings (enforced only post-event or for registered users)

Notifications

In-app messages with is_read status

Example: “You have successfully registered” or “Event starts soon”

Tech Stack
Language: Python 3.9+

Framework: Django 3+ & Django REST Framework

Database: SQLite (default) or PostgreSQL/MySQL for production

Authentication: djangorestframework-simplejwt

Deployed: PythonAnywhere or any WSGI-compatible hosting

Setup Instructions
Clone the repo:


git clone https://github.com/dprobity/eventmanagementapi.git
cd eventmanagementapi
Create & activate a virtual environment:

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
Install dependencies:


pip install -r requirements.txt
Environment Variables (Optional)


# In production, it’s recommended to configure:

SECRET_KEY = your Django secret key

DEBUG = set to False in production

ALLOWED_HOSTS = comma-separated list of domain names

You can store these in a .env file or set them on your hosting provider (e.g., PythonAnywhere).

# Running Migrations & Server
Apply migrations:


python manage.py makemigrations
python manage.py migrate
Create superuser:

python manage.py createsuperuser
Start the server:

python manage.py runserver
Visit http://127.0.0.1:8000/admin/ to access Django Admin.



# API Documentation
Below is an overview of all major endpoints and their functionality. By default, the base URL is http://127.0.0.1:8000/.

1. Authentication & Users
Endpoint	Method	Auth Required?	Description
/auth/register/	POST	No (public)	Register new user
/auth/login/	POST	No (public)	Obtain JWT tokens (access & refresh)
/auth/token/refresh/	POST	No (public)	Refresh JWT access token
/auth/me/	GET	Bearer Token (User)	Get your own user profile
/auth/me/	PUT	Bearer Token (User)	Update your profile
Note: If you want an endpoint to list all users or an admin-only route, create GET /auth/all/ with IsAdminUser.

2. Categories
Endpoint	Method	Auth Required?	Description
/categories/	GET	Optional (admin if create)	List all categories
/categories/	POST	Bearer Token (Admin recommended)	Create new category
/categories/<uuid:pk>/	GET	No	Retrieve single category detail (optional)
categories are read-only for normal users, while staff can create/edit.

3. Events
Endpoint	Method	Auth Required?	Description
/events/	GET	No	List upcoming events (search/filter/paginate)
/events/create/	POST	Bearer Token (IsOrganizer)	Create a new event
/events/<uuid:pk>/	GET	No	Get event details
/events/<uuid:pk>/edit/	PUT/DELETE	Bearer Token (Owner only)	Update/Delete an event you created
Filtering:


GET /events/?search=bootcamp
GET /events/?location=lagos
GET /events/?category=workshop
GET /events/?date_from=2025-01-01&date_to=2025-01-31
4. Registrations
Endpoint	Method	Auth Required?	Description
/registrations/	POST	Bearer Token (User)	Register for an event (includes quantity)
/registrations/mine/	GET	Bearer Token (User)	View all registrations (tickets) for current logged-in user
Key Points

# Waitlist Logic if event capacity is exceeded

# Multiple tickets with unique TicketInstance codes created automatically

# EventRegistration has status = registered or waitlisted

5. Feedbacks
Endpoint	Method	Auth Required?	Description
/feedbacks/	GET	No	List all feedback (or filter by ?event=<uuid>)
/feedbacks/	POST	Bearer Token (User)	Create new feedback (must be registered for the event)
/feedbacks/<uuid:pk>/	GET	No	Retrieve one feedback
/feedbacks/<uuid:pk>/	PUT	Bearer Token (Owner)	Update your feedback
/feedbacks/<uuid:pk>/	DELETE	Bearer Token (Owner)	Delete your feedback
Validation

Often restricted to users with EventRegistration(status='registered') and event date is past.

Ratings typically 1–5.

6. Notifications
Endpoint	Method	Auth Required?	Description
/notifications/	GET	Bearer Token (User)	List all notifications for logged-in user
/notifications/<uuid:pk>/mark-as-read/	PATCH	Bearer Token (Owner)	Mark a single notification as read
Creation

Often automatic on certain triggers, e.g. user registering for an event, event starts soon, etc.

Sample Requests & Responses
1) User Registration
Request (POST /auth/register/):

json

{
  "email": "john@example.com",
  "username": "john_doe",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "is_organizer": true
}
Response (201 Created):

json

{
  "email": "john@example.com",
  "username": "john_doe",
  "is_organizer": true
}
2) Creating an Event (Organizer)
Request (POST /events/create/, with Bearer token):

json

{
  "title": "Lagos Tech Bootcamp",
  "description": "3-day immersive coding event",
  "location": "Lagos, Nigeria",
  "date_time": "2025-08-01T09:00:00Z",
  "capacity": 50,
  "event_ticket_sells_off_soon": 5,
  "category": "<category_uuid>"
}
Response (201 Created):

json

{
  "id": "uuid-of-event",
  "title": "Lagos Tech Bootcamp",
  "description": "3-day immersive coding event",
  "location": "Lagos, Nigeria",
  "date_time": "2025-08-01T09:00:00Z",
  "capacity": 50,
  "registered_count": 0,
  "event_ticket_sells_off_soon": 5,
  "tickets_remaining": 50,
  "is_selling_out_soon": false,
  "is_active": true,
  "is_recurring": false,
  "organizer": "uuid-of-organizer",
  "category": "uuid-of-category",
  "created_at": "2025-03-31T..."
}
3) Register for an Event
Request (POST /registrations/, with Bearer token):

json

{
  "event": "<event_uuid>",
  "quantity": 3
}
Response (201 Created):

json

{
  "id": "uuid-of-registration",
  "user": "uuid-of-user",
  "event": "uuid-of-event",
  "quantity": 3,
  "status": "registered",
  "is_waitlisted": false,
  "created_at": "...",
  "ticket_instances": [
    { "id": "...", "code": "EVT-ABCD1234-1", "is_used": false },
    { "id": "...", "code": "EVT-ABCD1234-2", "is_used": false },
    { "id": "...", "code": "EVT-ABCD1234-3", "is_used": false }
  ]
}
Deployment Notes
PythonAnywhere is a great place to host this. Steps:

Upload your code or clone from GitHub.

Create a virtualenv & install dependencies.

Configure WSGI & domain in the Web tab.

python manage.py migrate & collectstatic (if using static files).

Reload the app, then test endpoints with your domain.

For production, consider:

A PostgreSQL database

DEBUG=False

Proper Allowed Hosts

Securing your Secret Key

License
This project is open-sourced under the MIT License – feel free to customize or adapt for your own use.