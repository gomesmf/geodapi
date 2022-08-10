test_accounts: export PYTHONPATH=${PWD}
test_accounts:
	cd accounts/tests && python3 -m unittest -v

test_distances: export SKIP_NOMINATIM_REQUEST=1
test_distances: export PYTHONPATH=${PWD}
test_distances:
	cd distances/tests && python3 -m unittest -v

test_nominatim: export PYTHONPATH=${PWD}
test_nominatim:
	cd distances/tests && python3 -m unittest -v test_nominatim

test_accounts_redisdb: export PYTHONPATH=${PWD}
test_accounts_redisdb:
	cd accounts/tests && python3 -m unittest -v test_redisdb

test_distances_redisdb: export PYTHONPATH=${PWD}
test_distances_redisdb:
	cd distances/tests && python3 -m unittest -v test_redisdb

test: test_accounts test_distances

test_redisdb: export SKIP_TEST_REDISDB=0
test_redisdb: test_accounts_redisdb test_distances_redisdb

updatereqs:
	python3 -m pip freeze > requirements.txt

PORT ?= 8000
runapi:
	python3 -m uvicorn api:app --reload --host 0.0.0.0 --port ${PORT}

genseckey:
	openssl rand -hex 32

runapp: PYTHONPATH=${PWD}
runapp:
	python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port ${PORT}

DG_IMGNAME = dgapi
DG_CNAME = dgapi
builddg:
	docker build -t ${DG_IMGNAME} -f ./Dockerfile .

rundg:
	docker run -d \
		--name ${DG_CNAME} \
		-p 8000:5000 \
		-v ${PWD}/app:/dg/app \
		${DG_IMGNAME}

bashdg:
	docker exec -it ${DG_CNAME} bash

rmfdg:
	docker rm -f ${DG_CNAME}

logsdg:
	docker logs --tail 1000 -f ${DG_CNAME}

cup:
	docker compose -f docker-compose.dev.yml up -d

cstop:
	docker compose -f docker-compose.dev.yml stop

crmf:
	docker compose -f docker-compose.dev.yml rm -f

cstoprmf: composestop composermf

ckill:
	docker compose -f docker-compose.dev.yml kill

cbashredis:
	docker exec -it dg-redis-1 sh

cbashdg:
	docker exec -it dg-api-1 bash

.PHONY: data
data:
	-mkdir -p data

redis: data
	-redis-server ./etc/redis.conf

redisshutdown:
	-redis-cli shutdown nosave

cleandata:
	rm -rf data

cleanpycache:
	find . -type d -name __pycache__ -exec rm -rf {} \;

cleandir: cleandata cleanpycache
