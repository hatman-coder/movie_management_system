# Movie Management System

This is a Django-based Movie Management System that allows users to manage movies, provide ratings, and includes an admin role for enhanced movie reporting. Authenticated users can securely log in, manage their movies, rate movies, and see an average rating for each movie.

## Table of Contents

- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Technologies](#technologies)
- [License](#license)

## Features

### 1. User Authentication
- Secure login using either username/password or email/password.
- Core features are accessible only to authenticated users.

### 2. Movie Management
- Authenticated users can create, view, update, and delete movies.
- Each movie is associated with the user who created it, allowing only the owner to make updates.

### 3. Rating System
- Users can rate any movie, update their rating, and see an average rating on each movie’s details page.

### 4. Admin Role
- Admin users have additional permissions to view and manage movie reports.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/movie-management-system.git
   cd movie-management-system
   ```

2. **Set up a Virtual Environment and Install Dependencies**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   - Run migrations to initialize the database:
     ```bash
     python manage.py migrate
     ```

4. **Create a Superuser**:
   - Set up an admin account:
     ```bash
     python manage.py createsuperuser
     ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**:
   - Open a browser and navigate to `http://127.0.0.1:8000`.

## Usage

- Register or log in to gain access to the application.
- Create, view, update, and manage your movies. Only the creator of a movie has permission to edit or delete it.
- Rate any movie and see its average rating.
- Admin users can manage and view movie reports.


## Technologies

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: Django Simple JWT
- **Deployment**: Docker (optional)


## License

This project is licensed under the MIT License.
Copyright (c) 2024 Tahseen Rahman
