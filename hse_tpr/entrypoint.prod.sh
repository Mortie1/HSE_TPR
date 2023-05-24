#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "<<< making migrations >>>"
python manage.py migrate --noinput
echo "<<< made migrations >>>"
echo "<<< collecting static >>>"
python manage.py collectstatic --noinput --clear
echo "<<< static collected >>>"

exec "$@"