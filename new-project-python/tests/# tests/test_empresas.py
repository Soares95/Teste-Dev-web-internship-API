# tests/test_empresas.py
import os
import pytest
from fastapi.testclient import TestClient
from main import app, Base, engine, SessionLocal
from main import Empresa

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_empresa(setup_db):
    response = client.post("/empresas/", json={
        "nome": "Empresa Teste",
        "cnpj": "12.345.678/0001-90",
        "endereco": "Rua Teste",
        "email": "email@teste.com",
        "telefone": "1234567890"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Empresa Teste"

def test_read_empresa(setup_db):
    response = client.get("/empresas/1")
    assert response.status_code == 200
    assert response.json()["nome"] == "Empresa Teste"

def test_update_empresa(setup_db):
    response = client.put("/empresas/1", json={
        "nome": "Empresa Atualizada",
        "cnpj": "12.345.678/0001-90",
        "endereco": "Rua Atualizada",
        "email": "email@atualizado.com",
        "telefone": "0987654321"
    })
    assert response.status_code == 200
    assert response.json()["nome"] == "Empresa Atualizada"

def test_delete_empresa(setup_db):
    response = client.delete("/empresas/1")
    assert response.status_code == 200
    assert response.json()["detail"] == "Empresa deletada com sucesso"
