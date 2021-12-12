.PHONY: lint format test build run clean init start install-hooks

help: ## prints all targets available and their description
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

dev-dependencies:  requirements-dev.txt ## install development dependencies
	pip install -r requirements-dev.txt

app-dependencies: requirements.txt ## install application dependencies
	pip install -r requirements.txt

all-dependencies: dev-dependencies	app-dependencies  ## install all dependencies

lint: ## check source code for style errors
	flake8 . && black . --check

format: ## automatic source code formatter following a strict set of standards
	isort . --sp .isort.cfg && black .


start: ## how to start develop
	@echo "************  How start develop ************"
	@echo "For create virtual environment:"
	@echo "python3 -m venv venv\\n"
	@echo "Install all dependencies:"
	@echo "make all-dependencies\\n"
	@echo "To start virtual dev environment:"
	@echo "source venv/bin/activate\\n"
	@echo "To exit of dev environment:"
	@echo "deactivate\\n"


install-hooks: ## installs git hooks in your local machine
	cp .pre-commit .git/hooks/pre-commit


