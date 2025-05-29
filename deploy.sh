#!/bin/bash

git add .
git stash
git fetch origin main
git reset --hard origin/main

docker compose -f docker-compose.production.yml down

docker compose -f docker-compose.production.yml up -d --build

sleep 10

docker compose -f docker-compose.production.yml exec web python manage.py collectstatic --noinput

if docker compose -f docker-compose.production.yml ps | grep -q "Up"; then
    docker compose -f docker-compose.production.yml ps
else
    docker compose -f docker-compose.production.yml logs
fi

echo "Done!"