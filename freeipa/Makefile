.PHONY: help
help: ## Format and display the manual pages
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

cret: ## Create Certificate
	docker exec -it freeipa bash /script/kinit.sh
	docker exec -it freeipa bash /script/setup-le.sh

rcret: ## Renew Certificate
	docker exec -it freeipa bash /script/kinit.sh
	docker exec -it freeipa bash /script/renew-le.sh

.PHONY: up
up: ## Create and start containers
	$(call docker-compose,up -d)

.PHONY: down
down: ## Stop and remove resources
	$(call docker-compose,down)

.PHONY: ps
ps: ## List containers
	$(call docker-compose,ps)

.PHONY: logs
logs: ## View output from containers
	$(call docker-compose,logs -f --tail 100)

.PHONY: clean
clean: ## Clean Elasticsearch data
	rm -rf freeipa

.PHONY: du
du: ## Containers down and up
	@make down
	@make up

.PHONY: dul
dul: ## Containers down and up and logs
	@make du
	@make logs

define docker-compose
    @docker-compose -f build/docker-compose.yml -p freeipa $1;
endef
