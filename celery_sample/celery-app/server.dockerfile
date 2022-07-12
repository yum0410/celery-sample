FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
WORKDIR /root

RUN pip install poetry

# opencv用ライブラリ
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev libglib2.0-0

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi
COPY . /app/