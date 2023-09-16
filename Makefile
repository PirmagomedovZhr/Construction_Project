local_up:
	docker-compose build
	docker-compose up -в

local_down:
	docker-compose down

test:
	docker-compose run --rm web sh -c "python manage.py test"

makemigrations:
	docker-compose run --rm web sh -c "python manage.py makemigrations"

migrate:
	docker-compose run --rm web sh -c "python manage.py migrate"

createsuperuser:
	docker-compose run --rm web sh -c "python manage.py createsuperuser"

