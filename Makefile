test: export PYTHONPATH=..
test:
	cd tests && python3 -m unittest -v

updatereqs:
	python3 -m pip freeze > requirements.txt

PORT ?= 8000
runapi:
	uvicorn api:app --reload --host 0.0.0.0 --port ${PORT}
