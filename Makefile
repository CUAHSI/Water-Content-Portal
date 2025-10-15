.PHONY: update
update:
	git submodule init
	git submodule update --remote

.PHONY: serve
serve:
	cd book && jupyter-book start

.PHONY: ci
ci:
	cd book && jupyter-book build --html --ci

.PHONY: clean
clean:
	jupyter-book clean --all --yes ./book/_build


.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make update                			- Update git submodules"
	@echo "  make serve                 			- Start a webserver serving the book locally"
	@echo "  make ci                				- Build the book in a non-interactive environment for CI"
	@echo "  make clean                 			- Clean any build outputs and artifacts"