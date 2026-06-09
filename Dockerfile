FROM python:3.12-slim

#install uv
COPY --from=ghrc.io/astral-sh/uv:latest /uv /uvx /bin/

# copy app to container
COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache