install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=main test_*.py
	# python -m pytest --nbval notebook.ipynb	#if you need to test a jupyter notebook

debug:
	python -m pytest -vv --pdb

format:
	black *.py

lint:
	pylint --disable=R,C --ignore-patterns=test_.*?py *.py

container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

refactor: format lint

deploy:
	#deploy goes here

all: install test refactor
