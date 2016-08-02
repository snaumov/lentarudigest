web: gunicorn news_parser.wsgi:application
worker: celery -A news_parser worker -B
