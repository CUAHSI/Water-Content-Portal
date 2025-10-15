.PHONY: update
update:
	git submodule init
	git submodule update --remote

# Start a webserver serving the book locally
.PHONY: serve
serve:
	cd book && jupyter-book start

# Clean any build outputs and artifacts
.PHONY: clean
clean:
	jupyter-book clean --all --yes ./book/_build


.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make update                			- Update git submodules"
	@echo "  make serve                 			- Start a webserver serving the book locally"
	@echo "  make clean                 			- Clean any build outputs and artifacts"