.PHONY: build
build:
	docker compose --profile serve build portal

.PHONY: build-docs
build-docs:
	docker compose --profile portal run --rm portal "mkdocs build"

.PHONY: serve
serve:
	docker compose --profile portal up portal

.PHONY: serve-d
serve-d:
	docker compose --profile portal up -d portal

.PHONY: shell
shell:
	docker compose --profile shell run --rm -ti portal-shell

.PHONY: down
down:
	docker compose down portal
