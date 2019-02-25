SERVICES=1
WORKERS=1

build:
	docker-compose build

pull:
	docker-compose pull

run:
	docker-compose up --scale rq-worker=$(WORKERS) --scale rq-service=$(SERVICES)

build-and-run:
	docker-compose up --build --scale rq-worker=$(WORKERS) --scale rq-service=$(SERVICES)
