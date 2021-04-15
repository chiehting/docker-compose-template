DOCKERDIR:=./docker
.DEFAULT_GOAL:=help

.PHONY: du
du: ## docker compose down,up.
	make down && make up

.PHONY: dul
dul: ## docker compose down,up,logs.
	make down && make up && make logs

up: ${DOCKERDIR}/docker-compose.yml
	$(call docker-compose,up -d)

down: ${DOCKERDIR}/docker-compose.yml
	$(call docker-compose,down)

ps: ${DOCKERDIR}/docker-compose.yml
	$(call docker-compose,ps)

logs: ${DOCKERDIR}/docker-compose.yml
	$(call docker-compose,logs -f --tail 100)

.PHONY: help
help: ## show help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST)|sed -E 's/[a-zA-Z_-]+://'|awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

define docker-compose
    @docker-compose -f ${DOCKERDIR}/docker-compose.yml -p haproxy $1;
endef

