.PHONY: help
help: ## Format and display the manual pages
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: up
up: ## Create and start containers
	mkdir -p data/grafana
	chmod 777 data/grafana
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
clean: ## Clean Grafana data
	rm -rf data/grafana

.PHONY: du
du: ## Containers down and up
	@make down
	@make up

.PHONY: dul
dul: ## Containers down and up and logs
	@make du
	@make logs

define docker-compose
    @docker-compose -f build/docker-compose.yml -p grafana $1;
endef
