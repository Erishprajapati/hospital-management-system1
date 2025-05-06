# Hospital Management System (HMS)

A fully functional Hospital Management System built using Django for the backend and Django Template for the frontend. This system helps manage patients, appointments, doctors, shifts, and provides an efficient way to store and access medical data. The system allows patients to book appointments, doctors to manage their shifts, and admins to monitor and manage the system.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
The Hospital Management System is designed to:
- Allow patients to register, view available doctors, and book appointments.
- Allow doctors to set available shifts and manage their schedules.
- Allow admins to manage the entire hospital system, view patient records, and assign doctors to appointments.

### Key Features:
- **Patient Management**: Register, view appointments, and manage patient data.
- **Doctor Shift Management**: Doctors can set and update their availability.
- **Appointment Management**: Patients can book appointments, and doctors can approve or reject them.
- **Admin Dashboard**: Admins can manage doctors, patients, and appointments.
- **Authentication**: Login, logout, and registration for patients and doctors.

## Features
- **Doctor Registration & Login**: Doctors can register their details, including specialization, phone number, and availability.
- **Patient Registration & Login**: Patients can register and view available doctors.
- **Appointment Booking**: Patients can select a doctor, book appointments, and receive confirmation.
- **Shift Management**: Doctors can update their availability, including shift timings.
- **Admin Panel**: Admin can manage doctors, patients, and appointments.
- **API Endpoints**: Expose APIs for interaction with the frontend.

## Tech Stack
- **Backend**: Django (Python)
  - Django Rest Framework for API creation
  - PostgreSQL
- **Frontend**: Django Template
- **Authentication**: Django's built-in authentication
- **Other Libraries**: 
  - `Bootstrap` for styling
  - `Axios` for making HTTP requests

## Setup & Installation

### Prerequisites
- Python 3.x
- Django
- PostgreSQL

### Backend (Django) Setup:
1. Clone the repository:
   ```bash
   git clone https://github.com/Erishprajapati/hospital-management-system.git
   cd hospital-management-system/backend
