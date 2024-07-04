# KANASTRA TEST

## Prerequisites

- Docker installed on your system.
- GNU Make installed on your system.
- Python 3.9+

## Makefile Targets

The Makefile in this project provides the following targets:

- `build` - Build the Docker image.
- `run-server` - Run server docker container.
- `run-db` - Run databse docker container.
- `stop` - Stop Docker container.
- `down` - Remove the Docker containers.
- `clean-db` - Remove the database Docker image and container and recreates it.

## Usage

### Creates an env-docker.sh file

To build docker and run database, you will need some env vars:

- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD

This repository have an env-docker.example, you can just copy and write the values that you want.

```sh
touch env-docker.sh
echo 'export POSTGRES_DB=kanastra
    export POSTGRES_USER=postgres
    export POSTGRES_PASSWORD=test
    export POSTGRES_PORT=5432

    export DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}' >> env-docker.sh
```

### Build the Docker Image

To build the Docker image, run the following command:

```sh
make build
```

### Run the Docker Container

To run the Docker container, ensuring any existing container with the same name is stopped and removed first, run:

```sh
make run-db
make run-server
```

### Stop the Docker Container

To stop the server and database, run:

```sh
make stop
```

### Clean Up database

To clean up the database and reinitialize, run:

```sh
make clean-db
```

## How to run tests

### Creates an env-docker.sh file

To build docker and run database, you will need some env vars:

- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD

This repository have an env-docker.example, you can just copy and write the values that you want.

```sh
touch env-docker.sh
echo 'export POSTGRES_DB=kanastra
    export POSTGRES_USER=postgres
    export POSTGRES_PASSWORD=test
    export POSTGRES_PORT=5432

    export DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${POSTGRES_PORT}/${POSTGRES_DB}' >> env-docker.sh
```

### Build the Docker Image

To build the Docker image, run the following command:

```sh
make build
```

### Run the database Docker Container

```sh
make run-db
```

### Creates virtualenv

To create a python virtualenv, run (you will need venv installed):

```sh
python3 -m venv env
source env/bin/activate
```

### Install the project packages

```sh
pip install -r requirements.txt
```

### Run the tests

```sh
pytest
```
