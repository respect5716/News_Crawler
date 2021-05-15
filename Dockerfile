FROM python:3.7

# Build essentials
RUN apt-get update
RUN apt-get install -yqq git

RUN git clone https://github.com/respect5716/News_Crawler.git


# Build app
WORKDIR News_Crawler
RUN pip install --no-cache-dir -r requirements.txt

COPY config.json config.json
CMD ["python", "main.py"]