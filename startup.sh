# Azure-specific startup script
#!/bin/bash

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate --noinput

# Start Gunicorn server
exec gunicorn --bind=0.0.0.0:$PORT --workers=4 --timeout=600 --access-logfile=- --error-logfile=- Aaarohan_Backend.wsgi:application