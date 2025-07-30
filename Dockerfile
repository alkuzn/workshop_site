FROM python:3.14.0rc1-alpine3.21
WORKDIR /app
RUN --mount=type=bind,src=requirements.txt,dst=/app/requirements.txt pip install -r requirements.txt
RUN --mount=type=tmpfs,dst=/app/ django-admin startproject t
COPY workshop_django_project/ /app/
CMD python3 -m uvicorn workshop_django_project.asgi:application --reload --host 0.0.0.0
