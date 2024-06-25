.PHONY: clean clean-build clean-pyc clean-test coverage dist docs help install lint lint/flake8 lint/black
.DEFAULT_GOAL := help

.ONESHELL:
ENV_PREFIX=.venv/bin/
PROJECT_NAME=src/metamoth

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache


fmt:              ## Format code using black & isort.
	$(ENV_PREFIX)ruff format $(PROJECT_NAME)/
	$(ENV_PREFIX)ruff format tests/

lint-pyright:
	$(ENV_PREFIX)pyright $(PROJECT_NAME)/

lint-ruff:
	$(ENV_PREFIX)ruff check $(PROJECT_NAME)/
	$(ENV_PREFIX)ruff check tests/ --ignore "D,E402"

lint: lint-pyright lint-ruff

test-watch:    ## Run tests and generate coverage report.
	$(ENV_PREFIX)ptw --runner "$(ENV_PREFIX)coverage run -m pytest -l --tb=long tests/" $(PROJECT_NAME)/ tests/

test:    ## Run tests and generate coverage report.
	$(ENV_PREFIX)pytest -s -vvv -l --tb=long --maxfail=1 tests/

coverage: ## check code coverage quickly with the default Python
	$(ENV_PREFIX)coverage run --source src -m pytest
	$(ENV_PREFIX)coverage report -m
	$(ENV_PREFIX)coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/metamoth.rst
	rm -f docs/modules.rst
	$(ENV_PREFIX)sphinx-apidoc -M -o docs/ src/metamoth
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	$(ENV_PREFIX)watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
