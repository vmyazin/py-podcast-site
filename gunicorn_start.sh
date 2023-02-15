#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/var/www/py-podcast-site/config
exec gunicorn -w 3 app:app

