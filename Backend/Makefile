# Use uv (https://github.com/astral-sh/uv)
UV = uv
PYTHON = python

# Default virtual environment directory
VENV = .venv

# Requirements files
REQ_APP = requirements/app.in
REQ_APP_LOCK = requirements/app.txt
REQ_DEV = requirements/dev.in
REQ_DEV_LOCK = requirements/dev.txt

.PHONY: install compile update sync run clean

compile-app:
	$(UV) pip compile $(REQ_APP) -o $(REQ_APP_LOCK)

compile-dev:
	$(UV) pip compile $(REQ_APP) $(REQ_DEV) -o $(REQ_DEV_LOCK)

compile: compile-app compile-dev

install: compile
	$(UV) pip install -r $(REQ_DEV_LOCK)

setup-uv:
	pip install uv

setup-lint:
	pre-commit

lint:
	pre-commit run --all-files

init: setup-uv install setup-lint
	echo "Creating everything"
