# SocialPost FastAPI

SocialPost FastAPI is a Python based API for managing social media posts. It provides endpoints for creating, updating, retrieving, and deleting posts or ideas.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Set up (without containers)](#local-installation)
  - [Set up with Containers](#local-run-containers)
- [API Documentation](#api-documentation)

## Features

- Create new social media posts with the pre-defined fields(schema) like title, content, visibility etc.
- Update, delete your posts. Only Author of the post can update/delete it.
- Read any post added by other users and vote for it if you like the post/idea.
- Authentication and authorization mechanisms (JWT Token Implementation) for secure usage.
- Sign Up and Sign In support to create user account.

## DB Set Up and updates using Alembic

- Alembic was used for this project for DB creation and updates (alembic incrementally track changes.)
- Refer the scripts under alembic folder and run `alembic upgrade head` to apply all the changes.
- `alembic upgrade` and `alembic downgrade` commands can be used as per reuirements.

## SQLAlchemy ORM for DB Object modeling

- In order to define the various DB tables SQLAlchemy was used.
- All the DB tables definitions are present under `models.py` file.

## Schema Validation with Pydantic

- In order to ensure strict schema for the posts and votes DB tables, Pydantic library was used.
- All the schema definitions are present under `schemas.py` file.


## Getting Started

### Prerequisites

All the dependecies are listed under requirements.txt. Major requirements are-
- Python (>= 3.6)
- FastAPI (>= 0.68)
- Postgres DB (locally installed if you are not using containers)
- Pydantic (>=1.10.7)
 

### Local Set up (without containers)

1. Clone the repository:

   ```bash
   git clone https://github.com/gigsbyips/socialpost-fast-api.git
   cd socialpost-fast-api
   ```

2. Create virtual Environment

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: venv\Scripts\activate.bat
    ```
3. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

4. Install prostgres and complete initial set up. Enter all the values like DB Name, user, password etc. in .env file which is read by config.py file (settings)

5. To run the application locally use below command.
    `uvicorn apps.main:app --host 0.0.0.0 --port 8000 --reload`

### Set up with Containers

- If you want to run this app on a remote server or say GitHub Code Build or EC2 instance where docker is availble then refer `docker-compose.yml` file

- If you want to run locally using containers then you can refer `docker-compose-dev.yml` file. Docker must be available on local for this to run.

## API Documentation
The API documentation is automatically generated using Swagger UI. You can access it by running the application and visiting http://localhost:8000/docs in your web browser.

The documentation provides details about available endpoints, request and response formats, and allows you to interact with the API directly.

## Maintainer
This repo is maintained by `Inderpal Singh` and the project was created to get faimilat with FastAPIs.
Feel free to fork and make changes in your repo. This is based on a free tutorial series by `Sanjeev T`.


