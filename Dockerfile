FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
EXPOSE 8000
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]

FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf
COPY html/ /usr/share/nginx/html
EXPOSE 80