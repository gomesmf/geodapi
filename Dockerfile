FROM python:3.8-slim

WORKDIR /geodapi

COPY ./requirements.txt /geodapi/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /geodapi/requirements.txt

COPY ./app /geodapi/app
COPY ./accounts /geodapi/accounts
COPY ./distances /geodapi/distances
COPY ./entrypoint.sh /geodapi/entrypoint.sh

CMD bash entrypoint.sh
