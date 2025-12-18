FROM python:3.11-slim
WORKDIR /app
COPY app.py /app/app.py
RUN pip install --no-cache-dir flask
RUN mkdir -p /data
EXPOSE 5001
CMD ["python", "app.py"]
