FROM python:3.9

WORKDIR /app

COPY ./sample_paper ./sample_paper
COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry install --no-root

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "sample_paper.app:app", "--host", "0.0.0.0", "--port", "8000"]