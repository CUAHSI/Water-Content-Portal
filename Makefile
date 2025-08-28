.PHONY: build
build:
	docker compose --profile portal build portal

.PHONY: build-docs
build-docs:
	docker compose --profile portal run --rm portal "source ~/.bashrc && mkdocs build"

.PHONY: serve
serve:
	docker compose --profile portal up portal 

.PHONY: serve-d
serve-d:
	docker compose --profile portal up -d portal

.PHONY: shell
shell:
	docker compose --profile shell run --rm -ti -p 8000:8000 portal-shell

.PHONY: down
down:
	docker compose down portal

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make build        - Build the portal Docker image"
	@echo "  make build-docs   - Build the MkDocs documentation"
	@echo "  make serve        - Serve the MkDocs documentation"
	@echo "  make serve-d      - Serve the MkDocs documentation in detached mode"
	@echo "  make shell        - Open a shell in the portal container"
	@echo "  make down         - Stop the portal container"
