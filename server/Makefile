export DB_HOST=127.0.0.1
export DB_PORT=8306

.PHONY: unit-tests
unit-tests: ## Run all unit tests
	current=$(pwd)
	PYTHONPATH=$current
	export PYTHONPATH
	echo $PYTHONPATH
	@echo "************ Unit Tests ************"
	python -m unittest discover -s tests/unit
