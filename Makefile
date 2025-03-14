# makefile for git-turf

.DEFAULT_GOAL = help
.PHONY: help
help: ## Show help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## install "git-turf"
	pip3 install -e .


.PHONY: uninstall
uninstall: ## uninstall "git-turf"
	pip3 uninstall git-turf

.PHONY: fonts
fonts: git_turf/font_data.py ## create font data
	cd misc ; make ; python3 conv_fonts.py > ../git_turf/font_data.py

.PHONY: test
test: ## run tests
	python3 -m mypy git_turf
	python3 setup.py test

.PHONY: venv
venv: ## create virtual environment
	python3 -m venv .venv

.PHONY: dev-install
dev-install: ## install for development(at venv)
	pip install -r requirements.txt
