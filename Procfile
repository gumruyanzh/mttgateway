web: gunicorn mtt_gateway.wsgi:application --log-file -
release: python manage.py collectstatic --noinput && python manage.py migrate 