.PHONY: lint format test build run clean init start install-hooks

NOW = $(shell date +"%Y%m%d%H%M%S")


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

.PHONY: new-migration
new-migration: ## creates a new migration file under "./migrations/scripts" with a timestamp, remember to rename the file to give it some context
	@FILE="./server/migrations/$(NOW)_rename_me.sql"; \
		touch $$FILE; \
		echo "Created file $$FILE, rename the 'rename_me' part to give the migration some context."

.PHONY: apply-migrations
apply-migrations: ## applies migrations to local database
	yoyo apply --batch --database mysql://root:datagos@localhost:8306/datagos ./server/migrations/
