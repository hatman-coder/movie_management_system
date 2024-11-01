FROM nginx/unit:1.28.0
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

COPY . /code/
COPY static /srv/www/movie_management/

RUN mkdir -p /code/log \
    && python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py collectstatic --no-input

EXPOSE 9430

CMD ["gunicorn", "--bind", "0.0.0.0:9430", "core.wsgi:application"]
