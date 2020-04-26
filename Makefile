test:
	pytest

lint:
	flake8 . --count --max-complexity=10 --max-line-length=127 --statistics

typecheck:
	mypy .

check-all: test lint typecheck

run-example:
	@python example/example.py
