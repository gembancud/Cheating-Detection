FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY databaserequirements.txt /code/
RUN pip install -r databaserequirements.txt
COPY . /code/