#!/bin/bash

export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres

docker-compose down
docker-compose build
docker-compose up

