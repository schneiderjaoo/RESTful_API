select

import unittest
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_database.db'
db = SQLAlchemy(app)


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    genre = db.Column(db.String(100))
    duration = db.Column(db.Integer)


class MusicSchema(SQLAlchemySchema):
    class Meta:
        model = Music
        load_instance = True

    id = auto_field()
    title = auto_field()
    artist = auto_field()
    genre = auto_field()
    duration = auto_field()


music_schema = MusicSchema()
music_schema_many = MusicSchema(many=True)


@app.route('/api/musicas/', methods=['GET'])
def get_musicas():
    musicas = Music.query.all()
    return music_schema_many.jsonify(musicas)


@app.route('/api/musicas/', methods=['POST'])
def create_musica():
    data = request.json
    title = data.get('title')
    artist = data.get('artist')
    genre = data.get('genre')
    duration = data.get('duration')

    musica = Music(title=title, artist=artist, genre=genre, duration=duration)
    db.session.add(musica)
    db.session.commit()

    return music_schema.jsonify(musica)


@app.route('/api/musicas/<int:music_id>', methods=['GET'])
def get_musica(music_id):
    musica = Music.query.get(music_id)
    return music_schema.jsonify(musica)


@app.route('/api/musicas/<int:music_id>', methods=['PATCH'])
def update_musica(music_id):
    musica = Music.query.get(music_id)
    data = request.json
    title = data.get('title', musica.title)
    artist = data.get('artist', musica.artist)
    genre = data.get('genre', musica.genre)
    duration = data.get('duration', musica.duration)

    musica.title = title
    musica.artist = artist
    musica.genre = genre
    musica.duration = duration

    db.session.commit()

    return music_schema.jsonify(musica)


@app.route('/api/musicas/<int:music_id>', methods=['DELETE'])
def delete_musica(music_id):
    musica = Music.query.get(music_id)
    db.session.delete(musica)
    db.session.commit()

    return jsonify(message='Música excluída com sucesso')


class APITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_database.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_musicas(self):
        response = self.app.get('/api/musicas/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 0)

    def test_create_musica(self):
        musica_data = {
            'title': 'Bohemian Rhapsody',
            'artist': 'Queen',
            'genre': 'Rock',
            'duration': 355
        }
        response = self.app.post('/api/musicas/', json=musica_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['title'], 'Bohemian Rhapsody')

    def test_get_musica(self):
        musica = Music(title='Bohemian Rhapsody', artist='Queen', genre='Rock', duration=355)
        db.session.add(musica)
        db.session.commit()

        response = self.app.get(f'/api/musicas/{musica.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['title'], 'Bohemian Rhapsody')

    def test_update_musica(self):
        musica = Music(title='Bohemian Rhapsody', artist='Queen', genre='Rock', duration=355)
        db.session.add(musica)
        db.session.commit()

        updated_data = {
            'title': 'New Title',
            'artist': 'Queen',
            'genre': 'Rock',
            'duration': 355
        }
        response = self.app.patch(f'/api/musicas/{musica.id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['title'], 'New Title')

    def test_delete_musica(self):
        musica = Music(title='Bohemian Rhapsody', artist='Queen', genre='Rock', duration=355)
        db.session.add(musica)
        db.session.commit()

        response = self.app.delete(f'/api/musicas/{musica.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['message'], 'Música excluída com sucesso')



class Gravadora(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))


class Artista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    gravadora_id = db.Column(db.Integer, db.ForeignKey('gravadora.id'))
    gravadora = db.relationship('Gravadora', backref='artistas')


class Genero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))


class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    cliente = db.relationship('Cliente', backref='pagamentos')
    valor = db.Column(db.Float)


class Plano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    valor_mensal = db.Column(db.Float)


class GravadoraSchema(SQLAlchemySchema):
    class Meta:
        model = Gravadora
        load_instance = True

    id = auto_field()
    nome = auto_field()


class ArtistaSchema(SQLAlchemySchema):
    class Meta:
        model = Artista
        load_instance = True

    id = auto_field()
    nome = auto_field()
    gravadora = auto_field()


class GeneroSchema(SQLAlchemySchema):
    class Meta:
        model = Genero
        load_instance = True

    id = auto_field()
    nome = auto_field()


class ClienteSchema(SQLAlchemySchema):
    class Meta:
        model = Cliente
        load_instance = True

    id = auto_field()
    nome = auto_field()


class PagamentoSchema(SQLAlchemySchema):
    class Meta:
        model = Pagamento
        load_instance = True

    id = auto_field()
    cliente = auto_field()
    valor = auto_field()


class PlanoSchema(SQLAlchemySchema):
    class Meta:
        model = Plano
        load_instance = True

    id = auto_field()
    nome = auto_field()
    valor_mensal = auto_field()


gravadora_schema = GravadoraSchema()
gravadora_schema_many = GravadoraSchema(many=True)

artista_schema = ArtistaSchema()
artista_schema_many = ArtistaSchema(many=True)

genero_schema = GeneroSchema()
genero_schema_many = GeneroSchema(many=True)

cliente_schema = ClienteSchema()
cliente_schema_many = ClienteSchema(many=True)

pagamento_schema = PagamentoSchema()
pagamento_schema_many = PagamentoSchema(many=True)

plano_schema = PlanoSchema()
plano_schema_many = PlanoSchema(many=True)


@app.route('/api/gravadoras/', methods=['GET'])
def get_gravadoras():
    gravadoras = Gravadora.query.all()
    return gravadora_schema_many.jsonify(gravadoras)


@app.route('/api/gravadoras/', methods=['POST'])
def create_gravadora():
    nome = request.json['nome']
    gravadora = Gravadora(nome=nome)
    db.session.add(gravadora)
    db.session.commit()
    return gravadora_schema.jsonify(gravadora)


@app.route('/api/artistas/', methods=['GET'])
def get_artistas():
    artistas = Artista.query.all()
    return artista_schema_many.jsonify(artistas)


@app.route('/api/artistas/', methods=['POST'])
def create_artista():
    nome = request.json['nome']
    gravadora_id = request.json['gravadora_id']
    artista = Artista(nome=nome, gravadora_id=gravadora_id)
    db.session.add(artista)
    db.session.commit()
    return artista_schema.jsonify(artista)


@app.route('/api/generos/', methods=['GET'])
def get_generos():
    generos = Genero.query.all()
    return genero_schema_many.jsonify(generos)


@app.route('/api/generos/', methods=['POST'])
def create_genero():
    nome = request.json['nome']
    genero = Genero(nome=nome)
    db.session.add(genero)
    db.session.commit()
    return genero_schema.jsonify(genero)


@app.route('/api/clientes/', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return cliente_schema_many.jsonify(clientes)


@app.route('/api/clientes/', methods=['POST'])
def create_cliente():
    nome = request.json['nome']
    cliente = Cliente(nome=nome)
    db.session.add(cliente)
    db.session.commit()
    return cliente_schema.jsonify(cliente)


@app.route('/api/pagamentos/', methods=['GET'])
def get_pagamentos():
    pagamentos = Pagamento.query.all()
    return pagamento_schema_many.jsonify(pagamentos)


@app.route('/api/pagamentos/', methods=['POST'])
def create_pagamento():
    cliente_id = request.json['cliente_id']
    valor = request.json['valor']
    pagamento = Pagamento(cliente_id=cliente_id, valor=valor)
    db.session.add(pagamento)
    db.session.commit()
    return pagamento_schema.jsonify(pagamento)


@app.route('/api/planos/', methods=['GET'])
def get_planos():
    planos = Plano.query.all()
    return plano_schema_many.jsonify(planos)


@app.route('/api/planos/', methods=['POST'])
def create_plano():
    nome = request.json['nome']
    valor_mensal = request.json['valor_mensal']
    plano = Plano(nome=nome, valor_mensal=valor_mensal)
    db.session.add(plano)
    db.session.commit()
    return plano_schema.jsonify(plano)


@app.route('/api/gravadoras/<int:gravadora_id>', methods=['GET'])
def get_gravadora(gravadora_id):
    gravadora = Gravadora.query.get(gravadora_id)
    return gravadora_schema.jsonify(gravadora)


@app.route('/api/gravadoras/<int:gravadora_id>', methods=['PATCH'])
def update_gravadora(gravadora_id):
    gravadora = Gravadora.query.get(gravadora_id)
    gravadora.nome = request.json['nome']
    db.session.commit()
    return gravadora_schema.jsonify(gravadora)


@app.route('/api/gravadoras/<int:gravadora_id>', methods=['DELETE'])
def delete_gravadora(gravadora_id):
    gravadora = Gravadora.query.get(gravadora_id)
    db.session.delete(gravadora)
    db.session.commit()
    return jsonify({'message': 'Gravadora excluída com sucesso'})


@app.route('/api/artistas/<int:artista_id>', methods=['GET'])
def get_artista(artista_id):
    artista = Artista.query.get(artista_id)
    return artista_schema.jsonify(artista)


@app.route('/api/artistas/<int:artista_id>', methods=['PATCH'])
def update_artista(artista_id):
    artista = Artista.query.get(artista_id)
    artista.nome = request.json['nome']
    artista.gravadora_id = request.json['gravadora_id']
    db.session.commit()
    return artista_schema.jsonify(artista)


@app.route('/api/artistas/<int:artista_id>', methods=['DELETE'])
def delete_artista(artista_id):
    artista = Artista.query.get(artista_id)
    db.session.delete(artista)
    db.session.commit()
    return jsonify({'message': 'Artista excluído com sucesso'})


@app.route('/api/generos/<int:genero_id>', methods=['GET'])
def get_genero(genero_id):
    genero = Genero.query.get(genero_id)
    return genero_schema.jsonify(genero)


@app.route('/api/generos/<int:genero_id>', methods=['PATCH'])
def update_genero(genero_id):
    genero = Genero.query.get(genero_id)
    genero.nome = request.json['nome']
    db.session.commit()
    return genero_schema.jsonify(genero)


@app.route('/api/generos/<int:genero_id>', methods=['DELETE'])
def delete_genero(genero_id):
    genero = Genero.query.get(genero_id)
    db.session.delete(genero)
    db.session.commit()
    return jsonify({'message': 'Gênero excluído com sucesso'})


@app.route('/api/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    return cliente_schema.jsonify(cliente)


@app.route('/api/clientes/<int:cliente_id>', methods=['PATCH'])
def update_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    cliente.nome = request.json['nome']
    db.session.commit()
    return cliente_schema.jsonify(cliente)


@app.route('/api/clientes/<int:cliente_id>', methods=['DELETE'])
def delete_cliente(cliente_id):
    cliente = Cliente.query.get(cliente_id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente excluído com sucesso'})


@app.route('/api/pagamentos/<int:pagamento_id>', methods=['GET'])
def get_pagamento(pagamento_id):
    pagamento = Pagamento.query.get(pagamento_id)
    return pagamento_schema.jsonify(pagamento)


@app.route('/api/pagamentos/<int:pagamento_id>', methods=['PATCH'])
def update_pagamento(pagamento_id):
    pagamento = Pagamento.query.get(pagamento_id)
    pagamento.cliente_id = request.json['cliente_id']
    pagamento.valor = request.json['valor']
    db.session.commit()
    return pagamento_schema.jsonify(pagamento)


@app.route('/api/pagamentos/<int:pagamento_id>', methods=['DELETE'])
def delete_pagamento(pagamento_id):
    pagamento = Pagamento.query.get(pagamento_id)
    db.session.delete(pagamento)
    db.session.commit()
    return jsonify({'message': 'Pagamento excluído com sucesso'})


@app.route('/api/planos/<int:plano_id>', methods=['GET'])
def get_plano(plano_id):
    plano = Plano.query.get(plano_id)
    return plano_schema.jsonify(plano)


@app.route('/api/planos/<int:plano_id>', methods=['PATCH'])
def update_plano(plano_id):
    plano = Plano.query.get(plano_id)
    plano.nome = request.json['nome']
    plano.valor_mensal = request.json['valor_mensal']
    db.session.commit()
    return plano_schema.jsonify(plano)


@app.route('/api/planos/<int:plano_id>', methods=['DELETE'])
def delete_plano(plano_id):
    plano = Plano.query.get(plano_id)
    db.session.delete(plano)
    db.session.commit()
    return jsonify({'message': 'Plano excluído com sucesso'})


class IntegrationTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_music_database.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_gravadora(self):
        # Cria uma gravadora
        gravadora_data = {'nome': 'Universal Music'}
        response = self.app.post('/api/gravadoras/', json=gravadora_data)
        gravadora = json.loads(response.data)

        # Verifica se a gravadora foi criada corretamente
        self.assertEqual(response.status_code, 200)
        self.assertEqual(gravadora['nome'], gravadora_data['nome'])

        # Obtém a gravadora criada
        response = self.app.get(f'/api/gravadoras/{gravadora["id"]}')
        gravadora = json.loads(response.data)

        # Verifica se a gravadora foi obtida corretamente
        self.assertEqual(response.status_code, 200)
        self.assertEqual(gravadora['nome'], gravadora_data['nome'])

        # Atualiza o nome da gravadora
        gravadora_data['nome'] = 'Sony Music'
        response = self.app.patch(f'/api/gravadoras/{gravadora["id"]}', json=gravadora_data)
        gravadora = json.loads(response.data)

        # Verifica se o nome da gravadora foi atualizado corretamente
        self.assertEqual(response.status_code, 200)
        self.assertEqual(gravadora['nome'], gravadora_data['nome'])

        # Deleta a gravadora
        response = self.app.delete(f'/api/gravadoras/{gravadora["id"]}')
        result = json.loads(response.data)

        # Verifica se a gravadora foi excluída corretamente
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['message'], 'Gravadora excluída com sucesso')

    # Métodos de teste para as outras classes

    def test_artista(self):
        pass

    def test_genero(self):
        pass

    def test_cliente(self):
        pass

    def test_pagamento(self):
        pass

    def test_plano(self):
        pass


if __name__ == '__main__':
    unittest.main()
