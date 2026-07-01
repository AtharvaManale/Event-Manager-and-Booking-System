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
- Two roles for users (user, organiser)
- Role checks for sensitive operations
- Organizer-only routes

### Event Management
- Only organisers can create, update, and delete events
- Only event organisers can modify/delete their own events
- Authenticated access to view events
- Ownership checks enforced at important changes

### Booking System
- Only users with the 'user' role can book events (limited to 1 seat per transaction)
- Users can view and cancel their own bookings (with ownership checks)
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

## Advanced Backend Design & Concurrency Control

### Pessimistic Concurrency Control (Row Locking)
- Simultaneous booking requests are serialized using SQLAlchemy's `with_for_update()` which places a write-lock (`SELECT ... FOR UPDATE` in MySQL) on the event row.
- This prevents race conditions, overbooking, and double-bookings when multiple users click the register button at the exact same millisecond.

### Temporary Seat Holds (Booking Cleanup Service)
- When a user tries to book, seats are temporarily marked as `PENDING_PAYMENT` for 15 minutes to allow time for the payment process.
- An automated `BookingCleanupService` is provided to check and release expired holds, returning the seats back to their events.
- This maintains high data consistency and prevents seats from being locked indefinitely.

### JWT Claims-Based Authorization
- User roles (user, organiser) are saved directly in the JWT as additional claims along with the user ID.
- This allows the backend to perform stateless, highly secure role checks on protected routes without hitting the database on every single request.

### API Pagination for Scalability
- The `/Events` feed endpoint utilizes server-side pagination with SQLAlchemy.
- It returns events in chunks (page-by-page) which keeps response times fast and reduces server memory overhead.

### Secure CORS Configuration
- Built-in Cross-Origin Resource Sharing (CORS) security is configured.
- This makes sure only trusted frontend origins can communicate with our API and prevents external malicious domains from triggering endpoints.

---

## API Modules

### Auth Routes
- User registration (roles are chosen here, either a user or an organiser)
- User login
- JWT token generation (access and refresh tokens with clean claims separation on refresh)
- JWT tokens will save user Id as identity and users role as additional claim for future ownership and role checks

### Event Routes
- First, user roles are checked (either user or organiser), and only organisers are allowed to access the features below
- Create event
- Update/Delete event (accessed only by the organiser who created that event)
- Get all events (accessed by all authenticated users)

### Booking Routes
- First, user roles are checked, and only users with the 'user' role are allowed to access the features below
- Book an event
- View user bookings
- View bookings for an event organiser
- Cancel a booking (restricted to the owner of the booking)

---

## SetUp Instructions
1. Clone the repo.
2. Create and activate a virtual environment.
3. Install Dependencies through this cli command

```bash
pip install -r requirments.txt
```

4. set environment variables (SECRET_KEY, JWT_SECRET_KEY, DATABASE_URL)
5. Initialize database through migrations cli commands

```bash
flask db init
flask db migrate
flask db upgrade
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
- Filtering
- Rate limiting
- Payment integration
- Deployment using Docker

### Author
Atharva Manale aka Apex Levo