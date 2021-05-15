FROM python:3.7

# Build essentials
RUN apt-get update
RUN apt-get install -yqq wget curl git unzip vim sudo


# Build app
VOLUME ["/app"]
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


EXPOSE 8888

CMD ["python", "main.py"]