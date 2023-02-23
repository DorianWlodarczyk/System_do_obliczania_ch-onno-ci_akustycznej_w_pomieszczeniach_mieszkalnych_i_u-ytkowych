#!/bin/bash

export POSTGRESS_USER=postgres
export POSTGRES_PASSWORD=postgres

docker-compose down
docker-compose build
docker-compose up

