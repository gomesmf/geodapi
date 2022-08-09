FROM python:3.8-slim

WORKDIR /dg

COPY ./requirements.txt /dg/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /dg/requirements.txt

COPY ./app /dg/app
COPY ./accounts /dg/accounts
COPY ./deliveries /dg/deliveries
COPY ./config.json /dg/config.json
COPY ./entrypoint.sh /dg/entrypoint.sh

CMD bash entrypoint.sh
