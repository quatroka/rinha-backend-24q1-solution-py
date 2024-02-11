FROM python:3.12.0-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN pip3 install -U pip poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /usr/src/app/

RUN poetry install --only main --no-root --no-interaction

COPY . /usr/src/app/

EXPOSE 3000

# CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "3000"]
CMD ["python", "-m", "gunicorn", "-c", "./gunicorn.conf.py"]
