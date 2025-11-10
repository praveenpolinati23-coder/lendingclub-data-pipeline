DOCKER_COMPOSE = docker compose -f infra/docker-compose.yml

# Build Docker image
build:
	$(DOCKER_COMPOSE) build

# Run Dagster UI
run:
	$(DOCKER_COMPOSE) up

# Stop and remove containers
down:
	$(DOCKER_COMPOSE) down

# Remove everything (optional clean up)
clean:
	$(DOCKER_COMPOSE) down -v --rmi all --remove-orphans
	rm -rf output/*

# Rebuild from scratch
rebuild: clean build run
