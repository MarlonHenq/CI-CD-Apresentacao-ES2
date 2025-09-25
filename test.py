import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from main import app, Base, engine, SessionLocal, User, UserCreate

client = TestClient(app)

# Setup e teardown do banco para testes
@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Limpa o banco antes e depois de cada teste"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Testes da classe User (SQLAlchemy)
def test_user_creation():
    """Testa criação de usuário no banco"""
    db = SessionLocal()
    user = User(name="Maria Santos")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    assert user.id is not None
    assert user.name == "Maria Santos"
    db.close()

def test_user_query():
    """Testa consulta de usuário"""
    db = SessionLocal()
    user = User(name="Pedro Silva")
    db.add(user)
    db.commit()
    user_id = user.id
    
    found_user = db.query(User).filter(User.id == user_id).first()
    assert found_user is not None
    assert found_user.name == "Pedro Silva"
    db.close()

# Testes da classe UserCreate (Pydantic)
def test_user_create_valid():
    """Testa criação de UserCreate válido"""
    user_data = UserCreate(name="Ana Costa")
    assert user_data.name == "Ana Costa"

def test_user_create_validation():
    """Testa validação com nome vazio"""
    with pytest.raises(ValidationError):
        UserCreate(name="")

def test_user_create_missing_name():
    """Testa UserCreate sem nome"""
    with pytest.raises(ValidationError):
        UserCreate()

# Testes dos endpoints da API funccionando
def test_create_user():
    """Testa criação de usuário via API"""
    response = client.post("/users/", json={"name": "João Silva"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "João Silva"
    assert "id" in data

def test_create_user_empty_name():
    """Testa criação com nome vazio"""
    response = client.post("/users/", json={"name": ""})
    assert response.status_code == 422

def test_create_user_missing_name():
    """Testa criação sem campo name"""
    response = client.post("/users/", json={})
    assert response.status_code == 422

def test_get_user():
    """Testar busca de usuário"""
    # cria usuário
    create_response = client.post("/users/", json={"name": "Carlos Lima"})
    user_id = create_response.json()["id"]

    # Busca usuário
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == user_id
    assert data["name"] == "Carlos Lima"

def test_get_user_not_found():
    """Testa busca de usuário inexistente"""
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"

def test_full_user_lifecycle():
    """Testa ciclo completo: criar -> buscar"""
    # Criar
    create_data = {"name": "Fernanda Santos"}
    create_response = client.post("/users/", json=create_data)
    assert create_response.status_code == 200
    
    user_id = create_response.json()["id"]
    
    # Buscar
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == create_data["name"]
