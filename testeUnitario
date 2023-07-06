import pytest
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import app, db, Music, Artist, Genero, Gravadora, Cliente, Plano

# Criar um cliente de teste para fazer as requisições à API
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Testes para a API Músicas
def test_listar_musicas(client):
    response = client.get('/api/musicas/')
    assert response.status_code == 200
    

def test_criar_musica(client):
    data = {
        "id": "1",
        "nome": "nome",
        "duracao": "160",
        "generos_id": "1",
        "lancamento": "1"
    }
    response = client.post('/api/musicas/', json=data)
    assert response.status_code == 200
    

def test_obter_informacoes_musica(client):
    music_id = 1
    response = client.get(f'/api/musicas/{music_id}')
    assert response.status_code == 200
    

def test_atualizar_musica(client):
    music_id = 1
    data = {
        "nome": "novo_nome"
    }
    response = client.patch(f'/api/musicas/{music_id}', json=data)
    assert response.status_code == 200
    

def test_excluir_musica(client):
    music_id = 1
    response = client.delete(f'/api/musicas/{music_id}')
    assert response.status_code == 200
    

# Testes para a API Gravadoras
def test_listar_gravadoras(client):
    response = client.get('/api/gravadora/')
    assert response.status_code == 200
    

def test_criar_gravadora(client):
    data = {
        "id": "1",
        "nome": "nome",
        "valor": "1",
        "vencimento": "21"
    }
    response = client.post('/api/gravadora/', json=data)
    assert response.status_code == 200
    

def test_obter_informacoes_gravadora(client):
    gravadora_id = 1
    response = client.get(f'/api/gravadora/{gravadora_id}')
    assert response.status_code == 200
    

def test_atualizar_gravadora(client):
    gravadora_id = 1
    data = {
        "nome": "novo_nome"
    }
    response = client.patch(f'/api/gravadora/{gravadora_id}', json=data)
    assert response.status_code == 200
    

def test_excluir_gravadora(client):
    gravadora_id = 1
    response = client.delete(f'/api/gravadora/{gravadora_id}')
    assert response.status_code == 200
    

# Testes para a API Artistas
def test_listar_artistas(client):
    response = client.get('/api/artistas/')
    assert response.status_code == 200
    

def test_criar_artista(client):
    data = {
        "id": "1",
        "nome": "nome",
        "gravadoras_id": "nome"
    }
    response = client.post('/api/artistas/', json=data)
    assert response.status_code == 200
    

def test_obter_informacoes_artista(client):
    artista_id = 1
    response = client.get(f'/api/artistas/{artista_id}')
    assert response.status_code == 200
    

def test_atualizar_artista(client):
    artista_id = 1
    data = {
        "nome": "novo_nome"
    }
    response = client.patch(f'/api/artistas/{artista_id}', json=data)
    assert response.status_code == 200
    

def test_excluir_artista(client):
    artista_id = 1
    response = client.delete(f'/api/artistas/{artista_id}')
    assert response.status_code == 200
    

# Testes para a API Gêneros
def test_listar_generos(client):
    response = client.get('/api/generos/')
    assert response.status_code == 200
    

def test_criar_genero(client):
    data = {
        "id": "1",
        "descricao": "descrição"
    }
    response = client.post('/api/generos/', json=data)
    assert response.status_code == 200
    

def test_obter_informacoes_genero(client):
    genero_id = 1
    response = client.get(f'/api/generos/{genero_id}')
    assert response.status_code == 200
    

def test_atualizar_genero(client):
    genero_id = 1
    data = {
        "descricao": "nova_descrição"
    }
    response = client.patch(f'/api/generos/{genero_id}', json=data)
    assert response.status_code == 200
    

def test_excluir_genero(client):
    genero_id = 1
    response = client.delete(f'/api/generos/{genero_id}')
    assert response.status_code == 200
    

# Testes para a API Clientes
def test_listar_clientes(client):
    response = client.get('/api/cliente/')
    assert response.status_code == 200
   

def test_criar_cliente(client):
    data = {
        "id": "1",
        "login": "login",
        "senha": "1",
        "email": "email",
        "plano": "nome"
    }
    response = client.post('/api/cliente/', json=data)
    assert response.status_code == 200
    

def test_obter_informacoes_cliente(client):
    cliente_id = 1
    response = client.get(f'/api/clientes/{cliente_id}')
    assert response.status_code == 200
    

def test_atualizar_cliente(client):
    cliente_id = 1
    data = {
        "login": "novo_login"
    }
    response = client.patch(f'/api/clientes/{cliente_id}', json=data)
    assert response.status_code == 200
    

def test_excluir_cliente(client):
    cliente_id = 1
    response = client.delete(f'/api/clientes/{cliente_id}')
    assert response.status_code == 200
    

# Testes para a API Pagamento
def test_listar_pagamentos(client):
    response = client.get('/api/pagamento/')
    assert response.status_code == 200
    

def test_criar_pagamento(client):
    data = {
        "id": "1",
        "data": "01/01/2023"
    }
    response = client.post('/api/pagamento/', json=data)
    assert response.status_code == 200
    

def test_obter_informacoes_pagamento(client):
    pagamento_id = 1
    response = client.get(f'/api/pagamento/{pagamento_id}')
    assert response.status_code == 200
    

def test_atualizar_pagamento(client):
    pagamento_id = 1
    data = {
        "data": "02/01/2023"
    }
    response = client.patch(f'/api/pagamento/{pagamento_id}', json=data)
    assert response.status_code == 200
    

def test_excluir_pagamento(client):
    pagamento_id = 1
    response = client.delete(f'/api/pagamento/{pagamento_id}')
    assert response.status_code == 200
    

# Testes para a API Plano
def test_listar_planos(client):
    response = client.get('/api/plano/')
    assert response.status_code == 200
    

def test_criar_plano(client):
    data = {
        "id": "1",
        "limite": "1",
        "valor": "1",
        "descricao": "descrição"
    }
    response = client.post('/api/plano/', json=data)
    assert response.status_code == 200
    

def test_obter_informacoes_plano(client):
    plano_id = 1
    response = client.get(f'/api/plano/{plano_id}')
    assert response.status_code == 200
    

def test_atualizar_plano(client):
    plano_id = 1
    data = {
        "descricao": "nova_descrição"
    }
    response = client.patch(f'/api/plano/{plano_id}', json=data)
    assert response.status_code == 200
    

def test_excluir_plano(client):
    plano_id = 1
    response = client.delete(f'/api/plano/{plano_id}')
    assert response.status_code == 200
    
