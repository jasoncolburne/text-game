test:
	pytest

lint:
	flake8 text_game --count --max-complexity=10 --max-line-length=127 --statistics

typecheck:
	mypy .

all: test lint typecheck
