.PHONY : venv test coverage build release

venv:
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	pip install -r requirements.txt

test:
	ruff check && \
	python3 -m unittest

coverage:
	coverage run --branch -m unittest
	coverage html

build:
	python3 -m build

release:
	.github/release.sh ${bump}