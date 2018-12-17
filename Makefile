dev:
	pipenv install --dev
	pipenv shell

deps:
	python3 -m pip install -r requirements.txt

run:
	python3 main.py

lint:
	pylint main.py
	pylint lib/*
	pylint lib/points/*
	pylint tests/*

test:
	python3 -m unittest discover tests 'test_*.py'
