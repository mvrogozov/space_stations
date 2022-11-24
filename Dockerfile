FROM python:3.9-slim-buster AS poetry
RUN python3 -m pip install --upgrade pip
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt

FROM python:3.9-slim-buster
WORKDIR /app
ENV IN_DOCKER=True
COPY --from=poetry /app/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["./space_stations/space/manage.py", "runserver", "0.0.0.0:8000"]