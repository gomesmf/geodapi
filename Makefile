test_accounts: export PYTHONPATH=../..
test_accounts:
	cd accounts/tests && python3 -m unittest -v

test_deliveries: export PYTHONPATH=../..
test_deliveries:
	cd deliveries/tests && python3 -m unittest -v

test: test_accounts test_deliveries

updatereqs:
	python3 -m pip freeze > requirements.txt

PORT ?= 8000
runapi:
	python3 -m uvicorn api:app --reload --host 0.0.0.0 --port ${PORT}
