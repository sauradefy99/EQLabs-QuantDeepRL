build:
	docker-compose build

up:
	docker-compose up --force-recreate

up-quiet:
	docker-compose up -d --force-recreate

run: build up

run-quiet: build up-quiet

down:
	docker-compose down
