test: export PYTHONPATH=..
test:
	cd tests && python3 -m unittest -v
