FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN groupadd --gid 10001 journal && useradd --uid 10001 --gid journal --no-create-home journal
COPY --chown=journal:journal . .
RUN install -d -o journal -g journal /app/data /app/staticfiles
USER journal
EXPOSE 8000
CMD ["sh", "-ec", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && exec gunicorn --bind 0.0.0.0:8000 --workers 2 --access-logfile - learning_log.wsgi:application"]
