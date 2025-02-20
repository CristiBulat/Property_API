# Property API

A simple CRUD API for managing real estate properties and their rooms. This API allows you to create, read, update, and delete properties and their rooms, along with listing them with pagination and filtering options. It also supports room management for each property.

## Features

- **CRUD Operations for Properties**: Create, read, update, and delete properties.
- **Room Management**: Add, update, delete, list and filter by area rooms for each property.
- **Pagination**: List properties with pagination.
- **Filtering**: Filter properties by price and location.
- **Error Handling**: Basic error handling for common scenarios.
- **Simple Authentication**: API key-based authentication can be implemented for restricted access.
- **SQLite Backend**: A simple SQLite database is used for storing property and room data.

## Tech Stack

- **FastAPI**: A modern web framework for building APIs with Python.
- **SQLAlchemy**: ORM for interacting with the SQLite database.
- **Pydantic**: For data validation and serialization.
- **SQLite**: A lightweight SQL database for storing property and room data.
- **OpenAPI**: Automatically generated documentation for the API.


### Clone the repository

```bash
git clone https://github.com/yourusername/property-api.git
cd property-api
