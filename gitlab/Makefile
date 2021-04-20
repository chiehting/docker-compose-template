.PHONY: help
help: ## Format and display the manual pages
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: rcret
rcret: ## Renew Certificate
	docker exec -it gitlab /bin/gitlab-ctl renew-le-certs

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

register: ## gitlab runner register
	docker exec -it gitlab-runner gitlab-runner register

.PHONY: clean
clean: ## Clean Gitlab data
	rm -rf d

.PHONY: du
du: ## Containers down and up
	@make down
	@make up

.PHONY: dul
dul: ## Containers down and up and logs
	@make du
	@make logs

define docker-compose
    @docker-compose -f build/docker-compose.yml -p gitlab $1;
endef
