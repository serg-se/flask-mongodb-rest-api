# Minimal RESTful API application with Flask and MongoDB

This repository offers an example of Flask application with REST API ready to be deployed on  Docker container.


#### RESTful endpoints

| HTTP Method | 	URI                                          | Description             |
|-------------|-----------------------------------------------|-------------------------|
| GET         | http://[hostname]/todo/api/v1.0/tasks	        | Retrieve list of tasks  |
| GET         | 	http://[hostname]/todo/api/v1.0/tasks/[_id]	 | Retrieve a task         |
| POST        | 	http://[hostname]/todo/api/v1.0/tasks	       | Create a new task       |
| PUT         | 	http://[hostname]/todo/api/v1.0/tasks/[_id]	 | Update an existing task |


#### Tech Stack:

* Web framework: Flask
* Database: MongoDB
* Parsing/Validation: Pydantic
* Containerization: Docker
* WSGI Server: Gunicorn

#### Features:

* Containerized Docker build
* Validation of data with Pydantic
* Tests covering each of the REST API
