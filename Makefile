.PHONY: update
update:
	git submodule init
	git submodule update --remote

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make update                - Update git submodules"
