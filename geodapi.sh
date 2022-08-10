#!/bin/bash

compose() {
    cat <<EOF > docker-compose.yml
version: "3.9"

services:
  api:
    image: "geodapi"
    ports:
      - "8000:5000"
    environment:
      - PWD_HASHING=passlib
      - DB_ACCOUNTS=redis
      - DB_DISTANCES=redis
      - REDIS_HOST=redis
      - SEARCH_SERVICE=nominatim
      - DISTANCE_SERVICE=geopy
  redis:
    image: "redis:alpine"
    volumes:
      - geodapiredis:/data
volumes:
  geodapiredis:

EOF
}

usage() {
    echo "usage: bash qbapi.sh [start|stop|kill|restart]"
}

volume() {
    docker volume create qbredis
}

start() {
    compose
    docker compose up -d
}

rmf() {
    docker compose rm -f
}

kill() {
    docker compose kill
}

stop() {
    docker compose stop
}

case $1 in
    start)
        start
        ;;
    stop)
        stop
        rmf
        ;;
    kill)
        kill
        rmf
        ;;
    restart)
        stop
        rmf
        start
        ;;
    *)
        usage
        ;;
esac
