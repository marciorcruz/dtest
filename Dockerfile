FROM python:3.11-slim

WORKDIR /app

# 1) Instala o netcat (versão openbsd) e limpa cache do apt
RUN apt-get update \
    && apt-get install -y netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# 2) Copia e instala as dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copia o resto da aplicação
COPY . /app/

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=dtest.settings

# 4) Garante que o entrypoint seja executável
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
