FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn


COPY . .

COPY nginx.conf /etc/nginx/sites-available/default

RUN python manage.py collectstatic --noinput

RUN python manage.py migrate

EXPOSE 80

CMD ["sh", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:8000 & nginx -g 'daemon off;'"]
