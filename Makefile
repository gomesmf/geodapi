test_accounts: export PYTHONPATH=${PWD}
test_accounts:
	cd accounts/tests && python3 -m unittest -v

test_deliveries: export SKIP_NOMINATIM_REQUEST=1
test_deliveries: export PYTHONPATH=${PWD}
test_deliveries:
	cd deliveries/tests && python3 -m unittest -v

test_nominatim: export PYTHONPATH=${PWD}
test_nominatim:
	cd deliveries/tests && python3 -m unittest -v test_nominatim

test: test_accounts test_deliveries

updatereqs:
	python3 -m pip freeze > requirements.txt

PORT ?= 8000
runapi:
	python3 -m uvicorn api:app --reload --host 0.0.0.0 --port ${PORT}
