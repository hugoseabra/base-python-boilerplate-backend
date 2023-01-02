DOCKER_COMPOSE_FILE=./docker-compose.yml
DB_SERVICE_NAME=postgres

.PHONY: help # Generate list of targets with descriptions
help:
	@grep '^.PHONY: .* #' Makefile | sed 's/\.PHONY: \(.*\) # \(.*\)/ - \1 - \2/'

#--------------------------------------- DB -----------------------------------
.PHONY: db_local_seed # Adds initial data to the system in local environment
db_local_seeds:
	@python manage.py loaddata 000_site
	@python manage.py loaddata 001_user

.PHONY: db_stock_seed # Adds Stock seeds to database
db_stock_seeds:
	@python manage.py loaddata 000_category
	@python manage.py loaddata 001_product

.PHONY: db_update # Updates database with fixtures
db_update:
	@python manage.py migrate
	@make db_local_seeds
	@make db_stock_seeds

.PHONY: db_flush # Destroys and recreates database services from scratch
db_flush:
	@docker-compose -p $(DOCKER_COMPOSE_FILE) -f $(DOCKER_COMPOSE_FILE) kill $(DB_SERVICE_NAME)
	@docker-compose -f $(DOCKER_COMPOSE_FILE) start $(DB_SERVICE_NAME)
	@sleep 10
	@make db_update
