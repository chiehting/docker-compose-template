.PHONY: help
help: ## Format and display the manual pages
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

up: ## Create and start containers
	$(call docker-compose,up -d)

down: ## Stop and remove resources
	$(call docker-compose,down)

ps: ## List containers
	$(call docker-compose,ps)

logs: ## View output from containers
	$(call docker-compose,logs -f --tail 100)

.PHONY: du
du: ## Containers down and up
	@make down
	@make up

.PHONY: dul
dul: ## Containers down and up and logs
	@make du
	@make logs

define docker-compose
    @docker-compose -f build/docker-compose.yml -p ansible $1;
endef
