FROM python:3.9-alpine
WORKDIR /app
COPY server.py /app/
CMD ["python", "/app/server.py"]