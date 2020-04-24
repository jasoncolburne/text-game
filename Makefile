test:
	pytest

lint:
	flake8 text_game --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 text_game --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

typecheck:
	mypy .

