#!/bin/sh


echo "***** RTE MODE: $RTE *****"


case "$RTE" in
    dev )
        echo "** Development mode."
        pip-audit
        coverage run --source="." --omit=manage.py manage.py test --verbosity 2
        coverage report -m
        python manage.py makemigrations --merge
        python manage.py migrate --noinput
        python manage.py runserver 0.0.0.0:8000

        ;;
    test )
        echo "** Test mode."
        pip-audit || exit 1
        coverage run --source="." --omit=manage.py manage.py test --verbosity 2
        coverage report -m --fail-under=90
      
        ;;
    prod )
        echo "** Production mode."
        python manage.py check --deploy
        python manage.py collectstatic --noinput
        gunicorn unepccc_project.asgi:application -b 0.0.0.0:8080 -k uvicorn.workers.UvicornWorker

        ;;
    * )
        echo "** Unknown mode."
        exit 1
        ;;
esac