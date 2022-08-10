#!/bin/bash

export PYTHONPATH=/geodapi

python3 -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-5000} --reload
