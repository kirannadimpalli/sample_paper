FROM python:3.9

WORKDIR /app

COPY ./sample_page ./sample_page
COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry install --no-root

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "sample_page.app:app", "--host", "0.0.0.0", "--port", "8000"]