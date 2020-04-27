test:
	pytest

lint:
	flake8 . --count --max-complexity=10 --max-line-length=127 --statistics

typecheck:
	mypy .

checks: test lint typecheck

run-example:
	@python example/example.py
