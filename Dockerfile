FROM python:3.11-slim

# Zainstaluj zależności systemowe
RUN apt-get update && apt-get install -y git build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY . /taiga-back
WORKDIR /taiga-back


# Zainstaluj wymagane pakiety Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Kopiuj własny config.py
COPY local.py /taiga-back/settings/local.py

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "taiga.wsgi:application"]