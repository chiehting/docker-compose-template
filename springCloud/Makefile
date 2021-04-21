DOCKERDIR:=./build
.DEFAULT_GOAL:=help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: build-all
build-all: ## build config、eureka、gateway、webclient、webservice
	make build-config
	make build-eureka
	make build-gateway
	make build-webclient
	make build-webservice

build-config: export service=config
build-config: ${DOCKERDIR}/maven.yml ## build config
	$(call build)

build-eureka: export service=eureka
build-eureka: ${DOCKERDIR}/maven.yml ## build eureka
	$(call build)

build-gateway: export service=gateway
build-gateway: ${DOCKERDIR}/maven.yml ## build web service
	$(call build)

build-webclient: export service=webclient
build-webclient: ${DOCKERDIR}/maven.yml ## build web client
	$(call build)

build-webservice: export service=webservice
build-webservice: ${DOCKERDIR}/maven.yml ## build web service
	$(call build)

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
clean: ## Clean Redmine data
	rm -rf config/target eureka/target gateway/target webclient/target webservice/target

define docker-compose
    @docker-compose -f ${DOCKERDIR}/docker-compose.yml -p springCloud $1;
endef

define build
    @docker-compose -f ${DOCKERDIR}/maven.yml up maven
    @docker-compose -f ${DOCKERDIR}/maven.yml down
endef

