FROM python:3.7

# Build essentials
RUN apt-get update
RUN apt-get install -yqq wget curl git unzip vim sudo cron


# Build app
VOLUME ["/app"]
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


EXPOSE 8888

#CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--port", "8888", "--allow-root"]
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]