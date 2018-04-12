FROM gliderlabs/alpine:3.4
ADD . /app
WORKDIR /app
CMD ["python", "app.py"]