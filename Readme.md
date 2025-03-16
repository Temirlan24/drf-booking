# Corporate Room Booking System

A web application for managing the reservation of meeting rooms in a corporate environment. This system allows employees to view available rooms, create bookings for specific time intervals, and manage their reservations. A custom user model (based on `AbstractBaseUser`) is used to handle employee-specific attributes such as department, position, and employee ID.

---

## Overview

- **Custom User Model**  
  Based on `AbstractBaseUser` and includes fields like `department`, `position`, `employee_id`, and contact information.  
  Utilizes **JWT** for authentication (access and refresh tokens).

- **Room Management**  
  Rooms have attributes such as `name`, `location`, `capacity`, and `equipment`.  
  Administrators can add, edit, or remove rooms.

- **Booking Flow**  
  Employees book rooms by specifying room ID, start time, and end time.  
  The system checks for conflicts to avoid overlapping bookings.  
  Users can view and manage (edit/cancel) their own bookings.

- **Notifications**  
  Sends email notifications about booking confirmations and cancellations (optional, depending on setup).

---

## API Endpoints

Below is an overview of the major API endpoints. Replace `<id>` with the resource ID and ensure requests include valid JWT tokens where required.

### 1. Authentication & User Management

| Endpoint                    | Method  | Description                                              |
|----------------------------|---------|----------------------------------------------------------|
| `/api/auth/register/`      | **POST**  | Register a new user. Expects fields like username, password, email, etc. |
| `/api/auth/token/`         | **POST**  | Obtain JWT (access & refresh tokens) using username + password.          |
| `/api/auth/token/refresh/` | **POST**  | Refresh access token using a valid refresh token.                        |
| `/api/users/profile/`      | **GET/PUT** | Get or update the current user's profile (email, department, position, etc.). |

### 2. Rooms

| Endpoint        | Method      | Description                                          |
|-----------------|------------|------------------------------------------------------|
| `/api/rooms/`   | **GET**     | Retrieve a list of all meeting rooms (public).      |
| `/api/rooms/`   | **POST**    | Add a new room (admin only).                        |
| `/api/rooms/<id>/` | **GET**  | Retrieve details of a specific room.                |
| `/api/rooms/<id>/` | **PUT/PATCH** | Edit details of an existing room (admin only).   |
| `/api/rooms/<id>/` | **DELETE**   | Delete a room (admin only).                        |

### 3. Bookings

| Endpoint               | Method       | Description                                                                                     |
|------------------------|-------------|-------------------------------------------------------------------------------------------------|
| `/api/bookings/`       | **GET**      | Retrieve a list of bookings owned by the currently authenticated user.                          |
| `/api/bookings/`       | **POST**     | Create a new booking. Expects `room` (ID), `start_time`, and `end_time`.                        |
| `/api/bookings/<id>/`  | **GET**      | Retrieve details of a specific booking.                                                         |
| `/api/bookings/<id>/`  | **PUT/PATCH**| Update a booking (e.g., change `start_time` or `end_time`).                                     |
| `/api/bookings/<id>/`  | **DELETE**   | Cancel a booking (only the owner or an admin can cancel). Status set to “canceled” or removed.  |

