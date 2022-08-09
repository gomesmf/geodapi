FROM python:3.8

WORKDIR /dg

COPY ./requirements.txt /dg/requirements.txt
RUN python3 -m install --no-cache-dir --upgrade -r /dg/requirements.txt

COPY ./app /dg/app
COPY ./accounts /dg/accounts
COPY ./deliveries /dg/deliveries
COPY ./entrypoint /dg/entrypoint.sh

CMD bash entrypoint.sh
