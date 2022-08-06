test_accounts: export PYTHONPATH=../..
test_accounts:
	cd accounts/tests && python3 -m unittest -v

test_distances: export PYTHONPATH=../..
test_distances:
	cd distances/tests && python3 -m unittest -v

updatereqs:
	python3 -m pip freeze > requirements.txt

PORT ?= 8000
runapi:
	uvicorn api:app --reload --host 0.0.0.0 --port ${PORT}
