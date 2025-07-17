DOCKERDIR:=./
.DEFAULT_GOAL:=help

.PHONY: help du dul up down ps logs clean

help: ## Format and display the manual pages
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST)|awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

du: ## Containers down and up
	make down && make up

dul: ## Containers down and up and logs
	make down && make up && make logs

up: ${DOCKERDIR}/docker-compose.yml ## Create and start containers
	mkdir -p data && chmod 777 data
	. .env
	$(call docker-compose,up -d)

down: ${DOCKERDIR}/docker-compose.yml ## Stop and remove resources
	$(call docker-compose,down)

ps: ${DOCKERDIR}/docker-compose.yml ## List containers
	$(call docker-compose,ps)

logs: ${DOCKERDIR}/docker-compose.yml ## View output from containers
	$(call docker-compose,logs -f --tail 100)

clean: ## Clean Redis data
	rm -rf data

define docker-compose
    @docker-compose -f ${DOCKERDIR}/docker-compose.yml -p n8n $1;
endef