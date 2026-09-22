SHELL := /bin/sh
PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: install test coverage lint format-check terraform-fmt-check terraform-validate check

install:
	$(PIP) install -r requirements.txt -r requirements-dev.txt

test:
	$(PYTHON) -m pytest -q

coverage:
	$(PYTHON) -m pytest --cov=app --cov=src --cov-report=term-missing --cov-report=xml --cov-fail-under=70

lint:
	$(PYTHON) -m ruff check .

format-check:
	$(PYTHON) -m ruff format --check .

terraform-fmt-check:
	terraform fmt -check -recursive infra

terraform-validate:
	@set -e; for dir in infra/envs/*; do \
		if [ -d "$$dir" ]; then \
			terraform -chdir="$$dir" init -backend=false -input=false; \
			terraform -chdir="$$dir" validate; \
		fi; \
	done

check: lint format-check test terraform-fmt-check terraform-validate
