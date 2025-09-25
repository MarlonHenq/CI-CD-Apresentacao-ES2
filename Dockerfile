FROM python:3.11-slim

WORKDIR /app

COPY main.py /app/

RUN pip install fastapi uvicorn sqlalchemy

# Expõe a porta 80
EXPOSE 80

# Comando para rodar a API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
