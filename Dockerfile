FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y \
    binutils libproj-dev gdal-bin postgis \
    gcc python3-dev musl-dev \
    libpq-dev \
    && apt-get clean

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "mozio_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
