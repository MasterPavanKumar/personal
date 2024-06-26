# Social Networking API

Connectico is a social networking app built using Django REST Framework. The API allows users to sign up, log in, search for other users, send and manage friend requests, and list friends.

## Features

- User Registration and Authentication
  - Sign up with email and password
  - Log in with email and password
- User Search
  - Search users by email or name
- Friend Requests
  - Send, accept, and reject friend requests
  - List friends
  - List pending friend requests

## Requirements

- Python 3.6+
- Django 3.2+
- Django REST Framework
- Django Simple JWT

## Setup

1. **Clone the repository:**

    git clone https://github.com/MasterPavanKumar/personal.git
    cd connectico
 
2. **Create a virtual environment and activate it:**

    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate.bat`

3. **Install the required packages:**

    pip install -r requirements.txt

4. **Run migrations:**

    python manage.py migrate

6. **Create a superuser (admin):**
    python manage.py createsuperuser

7. **Run the development server:**
    python manage.py runserver

## API Endpoints

### User Registration and Authentication

- **Sign Up**

    POST /connect/signup/

   Sample Request body:

    ```json
    {
        "email": "test@example.com",
        "password": "password",
        "name": "Test User"
    }
    ```

- **Log In**

    POST /connect/login/

    Sample Request body:

    ```json
    {
        "email": "test@example.com",
        "password": "password"
    }

### User Search

- **Search Users**
    GET /connect/users/search/?q=keyword
   

    Query Parameters:

    - `q`: The search keyword (either part of the name or the full email)

### Friend Requests

- **Send Friend Request**

    POST /connect/friends/request/

    Sample Request body:

    ```json
    {
        "to_user_id": "user_id"
    }
    ```

- **Accept Friend Request**

    POST /connect/friends/accept/

    Request body:

    ```json
    {
        "request_id": "request_id"
    }
    ```

- **Reject Friend Request**

    POST /connect/friends/reject/

    Request body:

    ```json
    {
        "request_id": "request_id"
    }
    ```

- **List Friends**

    GET /connect/friends/

- **List Pending Friend Requests**

    GET /connect/friends/requests/

## Expected Improvements
While the current implementation provides the basic functionality working, there is always room for improvement.

1.Better Authentication. Currently Implmented custom user and custom authentication, can be merged with Django's inbuilt function for better quality.
2.Better Token Expiration. Currently it is set to default 5 mins. Can be made better.
