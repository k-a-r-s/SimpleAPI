# FastAPI Simple API

## Overview

This is a simple API built with FastAPI, utilizing SQLAlchemy for ORM. The API allows for user management, post creation, voting, and login functionality.

## API Documentation

The API is documented using OpenAPI and can be accessed via:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Endpoints

### Users

- **GET /users/**  
  Retrieve all users.

- **POST /users/**  
  Create a new user.

- **GET /users/{id}**  
  Retrieve a user by ID.

- **DELETE /users/{id}**  
  Delete a user by ID.

### Posts

- **GET /posts/**  
  Retrieve all posts.

- **POST /posts/**  
  Create a new post.

- **GET /posts/{id}**  
  Retrieve a post by ID.

- **PUT /posts/{id}**  
  Update a post by ID.

- **DELETE /posts/{id}**  
  Delete a post by ID.

### Login

- **POST /login/**  
  User login.

### Votes

- **GET /votes/**  
  Retrieve all votes.

- **POST /votes/**  
  Cast a vote.

- **GET /votes/{post_id}**  
  Retrieve votes for a specific post.

### Home

- **GET /**  
  Home endpoint.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
# SimpleAPI
