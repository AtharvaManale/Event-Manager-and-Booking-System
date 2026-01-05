# Event Manager And Booking System Backend

## Overview
A backend system (Api system) for managing events and bookings, built using Flask and SQLAlchemy.
This project focuses on clean architecture, authentication, authorization, and real-world backend patterns rather than UI.

The system supports user authentication, role-based access control, event ownership, and secure booking workflows using JWT tokens.

---

## Tech Stack
- Python
- Flask
- Flask-JWT-Extended
- Flask-Migrate
- SQLAlchemy
- MySQL as database

---

## Core Features

### Authentication & Authorization
- JWT-based authentication (access tokens)
- Secure user registration and login
- Protected routes using JWT decorators
- Token-based user identity handling

### Role-Based Access Control
- Two roles for user (user, orgnaiser)
- Role checks for sensitive operations
- Admin-only and organizer-only routes

### Event Management
- Only organisers Create, update, and delete events
- Only event organisers can modify/delete events
- Public access to view events
- Ownership checks enforced at important changes

### Booking System
- only Users with role as user can book events
- Users can view their own bookings
- Event organisers can view bookings for their events

### Database & Migrations
- SQLAlchemy ORM for database modeling
- Flask-Migrate for schema migrations
- Clean separation of models and business logic

### API Design
- RESTful API structure
- Modular route blueprints
- Clear request and response formats
- Proper HTTP status codes and error handling

---

## API Modules

### Auth Routes
- User registration(roles are choosen here either an user or an orgainser)
- User login
- JWT token generation (access and refresh)
- JWT tokens will save user Id as identity and users role as additional claim for future ownership and role checks

### Event Routes
- Firstly at every routes roles will checked either an user or an orgainser and only organisers are allowes to access these below features
- Create event
- Update/Delete event (accessed only by the organiser of that event)
- Get all events (accessed by all users)
- Get single event details (accessed by all users)

### Booking Routes
- Firstly at every routes roles will checked either an user or an orgainser and only user are allowed to access below features
- Book an event
- View user bookings
- View bookings for an event organiser

---

## SetUp Instructions
1. Clone the repo.
2. Create and activate a virtual environment.
3. Install Dependencies through this cli command

```bash
pip install -r requirments.txt
```

4. set environment variables (SECRET_KEY, JWT_SECRET_KEY, DATABASE_URL)
5. Inialize database through migrations cli commands

```bash
flask db init
flask db migrate
flask bd upgarde
```
6. Runserver
```bash
cd Backend
python app.py
```
---

## Purpose of the Project(Learning Path)

### This project was built to:
- Strengthen backend fundamentals
- Practice authentication and authorization
- Understand real-world API design
- Prepare for backend and AI/ML system deployment work

#### The focus is on clean backend logic, security, and scalability, not frontend implementation.

### Future Improvements
- Pagination and filtering
- Rate limiting
- Payment integration
- Deployment using Docker

### Author
Atharva Manale aka Apex Levo