# API de Usuários - Projeto Simples Para mostrar CI/CD com Actions

API REST básica com FastAPI para demonstrar testes automatizados.

## 🛠️ Como usar

### Instalar dependências:
```bash
pip install fastapi sqlalchemy pydantic pytest httpx uvicorn
```

### Executar a aplicação:
```bash
uvicorn main:app --reload
```

### Executar testes:
```bash
python -m pytest test.py -v
```

## 📝 API Endpoints

**POST /users/** - Criar usuário
```json
{"name": "João Silva"}
```

**GET /users/{user_id}** - Buscar usuário

## 🐳 Docker

```bash
docker build -t api-usuarios .
docker run -p 8000:8000 api-usuarios
```