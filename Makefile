build:
	docker-compose build

run-server:
	docker-compose up web

run-db:
	docker-compose up db -d

stop:
	docker-compose stop

down:
	docker-compose down -v

clean-db:
	docker-compose down db -v
	docker-compose up db -d