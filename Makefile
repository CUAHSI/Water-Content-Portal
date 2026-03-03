.PHONY: update
update:
	git submodule init
	git submodule update --remote

.PHONY: sync
sync:
	git submodule sync --recursive

.PHONY: reset
reset:
	git reset --hard
	git submodule sync --recursive
	git submodule update --init --force --recursive
	git clean -ffdx
	git submodule foreach --recursive git clean -ffdx

.PHONY: serve
serve:
	cd book && jupyter-book start

.PHONY: ci
ci:
	cd book && jupyter-book build --html --ci

.PHONY: clean
clean:
	cd book && jupyter-book clean --all --yes ./_build


.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make update                			- Update git submodules"
	@echo "  make sync                				- Points local config to remote URLs defined in .gitmodules"
	@echo "  make serve                 			- Start a webserver serving the book locally"
	@echo "  make ci                				- Build the book in a non-interactive environment for CI"
	@echo "  make clean                 			- Clean any build outputs and artifacts"
	@echo "  make reset                 			- Cleans and resets a git repo and its submodules"