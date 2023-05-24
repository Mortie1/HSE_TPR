#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
echo "<<< making migrations >>>"
python manage.py makemigrations --noinput
echo "<<< migrating >>>"
python manage.py migrate --noinput
echo "<<< running setup.py >>>"
python manage.py shell < setup.py
echo "<<< success >>>"

exec "$@"