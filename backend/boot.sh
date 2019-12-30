#!/bin/sh

# initialize database
flask db init
flask db migrate
flask db upgrade

# start NGINX and Gunicorn
(exec nginx -g "daemon off;" 2>&1) &
exec gunicorn -b localhost:5000 --access-logfile - --error-logfile - backend:app
