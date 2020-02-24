build:
	docker-compose build

up:
	docker-compose up -d --force-recreate

run: build up

down:
	docker-compose down
