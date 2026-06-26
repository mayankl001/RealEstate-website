#!/bin/bash
echo "==> Building Project Dependencies..."
python3 -m pip install -r requirements.txt

echo "==> Collecting Static Files..."
python3 manage.py collectstatic --noinput --clear