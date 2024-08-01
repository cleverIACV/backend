#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files (only if you have static files)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Create a superuser if it doesn't exist (customize this part as needed)
echo "Creating superuser..."
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@admin.com', 'adminpass') if not User.objects.filter(username='admin').exists() else print('Superuser already exists.')" | python manage.py shell

# Start server
echo "Starting server..."
exec "$@"
