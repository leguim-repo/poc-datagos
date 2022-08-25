.PHONY: unit-tests
unit-tests: ## Run all unit tests
	current=$(pwd)
	PYTHONPATH=$current:"$current/app"
	export PYTHONPATH
	echo $PYTHONPATH
	@echo "************ Unit Tests ************"
	python -m unittest discover -s tests/unit
