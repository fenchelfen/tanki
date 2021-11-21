FROM python:3.10

RUN pip3 install poetry

WORKDIR /app
ADD pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction

COPY . /app

ENV PYTHONPATH=/app