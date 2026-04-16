FROM python:3.12.13-alpine3.23
WORKDIR /app
RUN --mount=type=bind,src=requirements.txt,dst=/app/requirements.txt pip install -r requirements.txt
COPY src/workshop_backend/ /app/
CMD python3 -m uvicorn config.asgi:application --host 0.0.0.0
