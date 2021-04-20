DOCKERDIR:=./build
.DEFAULT_GOAL:=help

.PHONY: help
help: ## Format and display the manual pages
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

init: build/ovpn-init.yml ## Initialization Services
	docker-compose -f build/ovpn-init.yml up
	docker-compose -f build/ovpn-init.yml down

.PHONY: du
du: ## Containers down and up
	make down && make up

.PHONY: dul
dul: ## Containers down and up and logs
	make down && make up && make logs

.PHONY: up
up: ## Create and start containers
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
clean: ## Clean OpenVPN data
	rm -rf data

.PHONY: client
client: ## Generate a client certificate without a passphrase
	docker exec -it ovpn rm -f /etc/openvpn/pki/reqs/${user}.req /etc/openvpn/pki/private/${user}.key /etc/openvpn/pki/issued/${user}.crt
	docker exec -it ovpn easyrsa build-client-full ${user} nopass
	docker exec -it ovpn ovpn_getclient ${user} > data/${user}.ovpn

define docker-compose
    @docker-compose -f ${DOCKERDIR}/docker-compose.yml -p openvpn $1;
endef

