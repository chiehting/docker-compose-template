DOCKERDIR:=.
.DEFAULT_GOAL:=help

.PHONY: help
help: ## Format and display the manual pages
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST)|awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: du
du: ## Containers down and up
	make down && make up

.PHONY: dul
dul: ## Containers down and up and logs
	make down && make up && make logs

.PHONY: up
up: ${DOCKERDIR}/docker-compose.yml ## Create and start containers
	$(call docker-compose,up -d)

.PHONY: down
down: ${DOCKERDIR}/docker-compose.yml ## Stop and remove resources
	$(call docker-compose,down)

.PHONY: ps
ps: ${DOCKERDIR}/docker-compose.yml ## List containers
	$(call docker-compose,ps)

.PHONY: logs
logs: ${DOCKERDIR}/docker-compose.yml ## View output from containers
	$(call docker-compose,logs -f --tail 100)

.PHONY: clean
clean: ## Clean Redis data
	rm -rf pgdocker socket

define docker-compose
    @docker-compose -f ${DOCKERDIR}/docker-compose.yml -p tdengine $1;
endef

