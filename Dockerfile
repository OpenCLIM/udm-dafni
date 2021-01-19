FROM python:3.8

RUN apt-get update && apt-get install -y swig

RUN mkdir /src
WORKDIR /src

COPY requirements.txt .
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "openudm", "/data/inputs/data"]