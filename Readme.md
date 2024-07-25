# Application Documentation

## Overview

This documentation provides an overview of the backend application built with FastAPI. The application utilizes JWT for authentication, with additional security measures by encrypting JWT tokens before sending them out and decrypting them upon return. The database used is PostgreSQL, Redis is employed for caching, and RQ is used for scheduling.

## Technology Stack

- **FastAPI**: The web framework used for building the application.
- **PostgreSQL**: The relational database management system used for storing data.
- **Redis**: An in-memory data structure store used for caching.
- **RQ**: An asynchronous task queue used for scheduling tasks.
- **JWT (JSON Web Tokens)**: Used for user authentication, with added encryption for enhanced security.

## Authentication

The application uses JWT for user authentication. To enhance security, JWT tokens are encrypted before being sent to the user and decrypted upon return.

### Token Encryption and Decryption

1. **Encryption**: Before sending the JWT token to the user, it is encrypted using a secure algorithm.
2. **Decryption**: When the token is received back from the user, it is decrypted to verify the user's identity and permissions.

## Database

### PostgreSQL

The application uses PostgreSQL as its primary database. PostgreSQL is a powerful, open-source object-relational database system that provides robust features and performance for handling complex queries and large datasets.

## Caching

### Redis

Redis is used for caching in the application. Redis is an in-memory data structure store that can be used as a database, cache, and message broker. Caching helps in improving the application's performance by storing frequently accessed data in memory, reducing the need to fetch data from the database repeatedly.

## Task Scheduling

### ARQ

RQ (Redis Queue) is used for scheduling tasks in the application. RQ is a high-performance, asyncio-compatible task queue that integrates seamlessly with FastAPI, allowing for the scheduling and execution of background tasks.
## Installation

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create virtual enviroment:

   ```sh
   python -m venv venv
   ```


3. Activate virtual enviroment:

   ```sh
   source venv/bin/activate
   ```

4. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

5. Set up environment variables:

   Create a `.env` file in the project root and add the necessary environment variables, such as database connection details, JWT secret key, and Redis connection details.

6. Run database migrations:

   ```sh
   alembic upgrade head
   ```

7. Start the application:

   ```sh
   uvicorn ai_health.root.app:app --reload --port 8010
   ```

## Usage

### Authentication

1. **Register**: Users can register by providing the necessary details. A JWT token is generated and sent to the user upon successful registration.

2. **Login**: Users can log in by providing their credentials. A JWT token is generated, encrypted, and sent to the user.

3. **Access Protected Routes**: Users can access protected routes by including the JWT token in the `Authorization` header of the request.

### Caching

Frequently accessed data is cached in Redis to improve performance. The caching layer ensures that data is served quickly without repeatedly querying the database.

### Task Scheduling

Background tasks are scheduled and executed using ARQ. These tasks can include sending emails, processing data, and other asynchronous operations.
