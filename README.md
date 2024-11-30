# WeatherData Project 🌦️

A weather data visualization and management application built with **Vue.js**, **FastAPI**, and **PostgreSQL**. This project allows users to register/login, interact with a secure backend, and visualize weather data such as maximum temperatures for specific stations using charts.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **User Authentication**: JWT-based secure login and registration.
- **Protected Routes**: Users must be authenticated to access specific parts of the application.
- **Interactive Charts**: Visualize weather data (e.g., maximum temperatures by station).
- **REST API**: Built with FastAPI to manage weather data and user authentication.
- **Responsive UI**: Designed for both desktop and mobile devices.

---

## Tech Stack

**Frontend**:
- [Vue.js](https://vuejs.org/) - Framework for building the UI.
- [Chart.js](https://www.chartjs.org/) - For data visualization (temperature graphs).

**Backend**:
- [FastAPI](https://fastapi.tiangolo.com/) - High-performance Python framework for APIs.
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM.
- [PostgreSQL](https://www.postgresql.org/) - Database for storing weather data and user information.

---


---

## Setup Instructions


### Backend Setup

1. **Navigate to the backend directory**:

   cd backend

2. **Create a Python virtual environment**:

    python -m venv venv
    source venv/bin/activate   # Use `venv\Scripts\activate` on Windows

3. **Install dependencies**:

    pip install -r requirements.txt

4. **Set up the PostgreSQL database**:

    Create a PostgreSQL database named weatherdata.
    Add your connection details to the .env file (see Environment Variables).

5. **Run database migration**:

    python initialize_users.py

6. **Start the backend server**:

    uvicorn main:app --reload

### Database Setup

1. **Navigate to the scrpit directory**:

    cd script

2. **Set up the database data**:

    python download_data.py
    python create_table.py
    python import_data.py

### Frontend Setup

1. **Navigate to the frontend directory**:

   cd frontend

2. **Install dependencies**:

    npm install

3. **Run the Vue.js development server**:

    npm run serve
