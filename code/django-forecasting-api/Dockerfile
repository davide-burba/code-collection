FROM python:3.9-slim-buster

RUN mkdir /code

COPY poetry.lock /code/
COPY pyproject.toml /code/
COPY project /code/project

WORKDIR /code/project/

RUN apt-get update
RUN apt-get install libgomp1
RUN pip install poetry && poetry config virtualenvs.create false 
RUN poetry install --no-root

CMD ./manage.py runserver 0.0.0.0:8000
