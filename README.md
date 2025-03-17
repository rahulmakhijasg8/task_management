# High-Performance Task Management System

A scalable and robust task management system built with Django, Django REST Framework, PostgreSQL, Redis, and Celery. This system allows users to create, assign, and track tasks with real-time updates and asynchronous processing capabilities.

## Features

### User Management
- JWT-based authentication
- User registration and profile management
- Role-based access control

### Task Management
- Create, read, update, and delete tasks
- Task assignment to users
- Advanced filtering and pagination
- Priority and status tracking

### High-Performance Processing
- Multi-threaded report generation for handling 100,000+ tasks
- Asynchronous notifications using Celery and Redis
- Real-time updates via WebSockets (Django Channels)
- Response caching for optimized performance

### Additional Features
- Rate limiting to prevent API abuse
- Asynchronous task export to CSV

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Caching & Message Broker**: Redis
- **Asynchronous Processing**: Celery
- **Real-time Communication**: Django Channels, WebSockets
- **Containerization**: Docker

## System Architecture

```
┌───────────────┐      ┌───────────────┐      ┌───────────────┐
│   Django API  │◄────►│   PostgreSQL  │      │ Redis (Cache) │
└───────┬───────┘      └───────────────┘      └───────┬───────┘
        │                                             │
        │                                             │
┌───────▼───────┐      ┌───────────────┐      ┌───────▼───────┐
│Django Channels│◄────►│   WebSockets  │      │ Celery Worker │
└───────────────┘      └───────────────┘      └───────────────┘
```

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rahulmakhijasg8/task_management.git
cd task_management
```

3. Build and start the Docker containers:
```bash
docker-compose up --build
```

4. Create a superuser (optional):
```bash
docker-compose exec web python manage.py createsuperuser
```

6. Access the API at `http://localhost:8000/` and the admin panel at `http://localhost:8000/admin/`

## API Documentation

### Authentication

#### Register a new user
```
POST /register/
```

#### Refresh token
```
POST /api/token/refresh/
```

#### Access token
```
POST /api/token/
```

### Task Management

#### List tasks (with pagination and filtering)
```
GET /api/tasks/?status=pending&priority=high&page=1
```

#### Create a task
```
POST /tasks/
```

#### Retrieve a task
```
GET /tasks/{id}/
```

#### Update a task
```
PUT /tasks/{id}/
```

#### Delete a task
```
DELETE /tasks/{id}/
```

### Reports

#### Generate task analytics report
```
GET /report/
```