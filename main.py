from datetime import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=False, nullable=False)
    duracao = db.Column(db.Integer, nullable=False)
    generos_id = db.Column(db.Integer, nullable=False)
    lancamento = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id, nome, duracao, generos_id, lancamento):
        self.id = id
        self.nome = nome
        self.duracao = duracao
        self.generos_id = generos_id
        self.lancamento = lancamento


class MusicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Music
        include_fk = True
        load_instance = True


music_schema = MusicSchema()
music_schemas = MusicSchema(many=True)


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=False, nullable=False)
    gravadoras_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id, nome, gravadoras_id):
        self.id = id
        self.nome = nome
        self.gravadoras_id = gravadoras_id


class ArtistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Artist
        include_fk = True
        load_instance = True


artist_schema = ArtistSchema()
artist_schemas = ArtistSchema(many=True)


class Genero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(120), unique=False, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id, descricao):
        self.id = id
        self.descricao = descricao


class GeneroSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Genero
        include_fk = True
        load_instance = True


genero_schema = GeneroSchema()
genero_schemas = GeneroSchema(many=True)


class Gravadora(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=False, nullable=False)
    valor = db.Column(db.Integer, nullable=False)
    vencimento = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id, nome, valor, vencimento):
        self.id = id
        self.nome = nome
        self.valor = valor
        self.vencimento = vencimento


class GravadoraSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Gravadora
        include_fk = True
        load_instance = True


gravadora_schema = GravadoraSchema()
gravadora_schemas = GravadoraSchema(many=True)


class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(45), unique=True, nullable=False)
    senha = db.Column(db.String(45), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    planos_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def __init__(self, id, login, senha, planos_id, email):
        self.id = id
        self.login = login
        self.senha = senha
        self.email = email
        self.planos_id = planos_id


class ClienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        include_fk = True
        load_instance = True


cliente_schema = ClienteSchema()
cliente_schemas = ClienteSchema(many=True)


class Plano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(45), unique=False, nullable=False)
    valor = db.Column(db.Float(precision=2), nullable=False)
    limite = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id, descricao, valor, limite):
        self.id = id
        self.descricao = descricao
        self.valor = valor
        self.limite = limite


class PlanoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Plano
        include_fk = True
        load_instance = True


plano_schema = PlanoSchema()
plano_schemas = PlanoSchema(many=True)


class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, id):
        self.id = id


class PagamentoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pagamento
        include_fk = True
        load_instance = True


pagamento_schema = PagamentoSchema()
pagamento_schemas = PagamentoSchema(many=True)

with app.app_context():
    db.create_all()


@app.route("/api/musicas/", methods=['GET', 'POST'])
def musicas():
    if request.method == 'GET':
        all_music = Music.query.all()

        return jsonify(music_schemas.dump(all_music))
    elif request.method == 'POST':
        new_music = request.get_json()
        music = Music(new_music['id'],new_music['nome'], new_music['duracao'], new_music['generos_id'], new_music['lancamento'])

        db.session.add(music)
        db.session.commit()

        return jsonify({'message': 'Música criada com sucesso!'}), 201


@app.route("/api/musicas/<int:music_id>", methods=['GET', 'PATCH', 'DELETE'])
def musicas_by_id(music_id):
    if request.method == 'GET':
        music = Music.query.get(music_id)

        if music is None:
            return jsonify({'message': 'Música não encontrada!'}), 404

        return jsonify(music_schema.dump(music))
    elif request.method == 'PATCH':
        music = Music.query.get(music_id)

        if music is None:
            return jsonify({'message': 'Música não encontrada para atualização!'}), 404

        update_data = request.get_json()

        music.nome = update_data.get('nome', music.nome)
        music.duracao = update_data.get('duracao', music.duracao)
        music.generos_id = update_data.get('generos_id', music.generos_id)
        music.lancamento = update_data.get('lancamento', music.lancamento)

        db.session.commit()

        return jsonify({'message': 'Música atualizada com sucesso!'})
    elif request.method == 'DELETE':
        music = Music.query.get(music_id)

        if music is None:
            return jsonify({'message': 'Música não encontrada para deletar!'}), 404

        db.session.delete(music)
        db.session.commit()

        return jsonify({'message': 'Música deletada com sucesso!'}), 204


@app.route("/api/artistas/", methods=['GET', 'POST'])
def artistas():
    if request.method == 'GET':
        all_artist = Artist.query.all()

        return jsonify(artist_schemas.dump(all_artist))
    elif request.method == 'POST':
        new_artist = request.get_json()
        artist = Artist(new_artist['nome'], new_artist['gravadoras_id'])

        db.session.add(artist)
        db.session.commit()

        return jsonify({'message': 'Artista criado com sucesso!'}), 201


@app.route("/api/artistas/<int:artist_id>", methods=['GET', 'PATCH', 'DELETE'])
def artistas_by_id(artist_id):
    if request.method == 'GET':
        artist = Artist.query.get(artist_id)

        if artist is None:
            return jsonify({'message': 'Artista não encontrado!'}), 404

        return jsonify(artist_schema.dump(artist))
    elif request.method == 'PATCH':
        artist = Artist.query.get(artist_id)

        if artist is None:
            return jsonify({'message': 'Artista não encontrado para atualização!'}), 404

        update_data = request.get_json()

        artist.nome = update_data.get('nome', artist.nome)
        artist.gravadoras_id = update_data.get('gravadoras_id', artist.gravadoras_id)

        db.session.commit()

        return jsonify({'message': 'Artista atualizado com sucesso!'})
    elif request.method == 'DELETE':
        artist = Artist.query.get(artist_id)

        if artist is None:
            return jsonify({'message': 'Artista não encontrado para deletar!'}), 404

        db.session.delete(artist)
        db.session.commit()

        return jsonify({'message': 'Artista deletado com sucesso!'}), 204


@app.route("/api/generos/", methods=['GET', 'POST'])
def generos():
    if request.method == 'GET':
        all_genero = Genero.query.all()

        return jsonify(genero_schemas.dump(all_genero))
    elif request.method == 'POST':
        new_genero = request.get_json()
        genero = Genero(new_genero['id'], new_genero['descricao'])

        db.session.add(genero)
        db.session.commit()

        return jsonify({'message': 'Genero criado com sucesso!'}), 201


@app.route("/api/generos/<int:genero_id>", methods=['GET', 'PATCH', 'DELETE'])
def generos_by_id(genero_id):
    if request.method == 'GET':
        genero = Genero.query.get(genero_id)

        if genero is None:
            return jsonify({'message': 'Genero não encontrado!'}), 404

        return jsonify(genero_schema.dump(genero))
    elif request.method == 'PATCH':
        genero = Genero.query.get(genero_id)

        if genero is None:
            return jsonify({'message': 'Genero não encontrado para atualização!'}), 404

        update_data = request.get_json()

        genero.id = update_data.get('id', genero.id)
        genero.descricao = update_data.get('descricao', genero.descricao)

        db.session.commit()

        return jsonify({'message': 'Genero atualizada com sucesso!'})
    elif request.method == 'DELETE':
        genero = Genero.query.get(genero_id)

        if genero is None:
            return jsonify({'message': 'Genero não encontrado para deletar!'}), 404

        db.session.delete(genero)
        db.session.commit()

        return jsonify({'message': 'Genero deletado com sucesso!'}), 204


@app.route("/api/gravadora/", methods=['GET', 'POST'])
def gravadora():
    if request.method == 'GET':
        all_gravadora = Gravadora.query.all()

        return jsonify(gravadora_schemas.dump(all_gravadora))
    elif request.method == 'POST':
        new_gravadora = request.get_json()
        gravadora = Gravadora(new_gravadora['id'], new_gravadora['nome'], new_gravadora['valor'],
                              new_gravadora['vencimento'])

        db.session.add(gravadora)
        db.session.commit()

        return jsonify({'message': 'Gravadora criada com sucesso!'}), 201


@app.route("/api/gravadora/<int:gravadora_id>", methods=['GET', 'PATCH', 'DELETE'])
def gravadora_by_id(gravadora_id):
    if request.method == 'GET':
        gravadora = Gravadora.query.get(gravadora_id)

        if gravadora is None:
            return jsonify({'message': 'Gravadora não encontrada!'}), 404

        return jsonify(gravadora_schema.dump(gravadora))
    elif request.method == 'PATCH':
        gravadora = Gravadora.query.get(gravadora_id)

        if gravadora is None:
            return jsonify({'message': 'Gravadora não encontrada para atualização!'}), 404

        update_data = request.get_json()

        gravadora.id = update_data.get('id', gravadora.id)
        gravadora.nome = update_data.get('nome', gravadora.nome)
        gravadora.valor = update_data.get('valor', gravadora.valor)
        gravadora.vencimento = update_data.get('vencimento', gravadora.vencimento)

        db.session.commit()

        return jsonify({'message': 'Gravadora atualizada com sucesso!'})
    elif request.method == 'DELETE':
        gravadora = Gravadora.query.get(gravadora_id)

        if gravadora is None:
            return jsonify({'message': 'Gravadora não encontrada para deletar!'}), 404

        db.session.delete(gravadora)
        db.session.commit()

        return jsonify({'message': 'Gravadora deletada com sucesso!'}), 204


@app.route("/api/clientes/", methods=['GET', 'POST'])
def clientes():
    if request.method == 'GET':
        all_cliente = Cliente.query.all()

        return jsonify(cliente_schemas.dump(all_cliente))
    elif request.method == 'POST':
        new_cliente = request.get_json()
        cliente = Cliente(new_cliente['id'], new_cliente['login'], new_cliente['senha'], new_cliente['planos_id'],
                          new_cliente['email'])

        db.session.add(cliente)
        db.session.commit()

        return jsonify({'message': 'Cliente criado com sucesso!'}), 201


@app.route("/api/clientes/<int:cliente_id>", methods=['GET', 'PATCH', 'DELETE'])
def cliente_by_id(cliente_id):
    if request.method == 'GET':
        cliente = Cliente.query.get(cliente_id)

        if cliente is None:
            return jsonify({'message': 'Cliente não encontrado!'}), 404

        return jsonify(cliente_schema.dump(cliente))
    elif request.method == 'PATCH':
        cliente = Cliente.query.get(cliente_id)

        if cliente is None:
            return jsonify({'message': 'Música não encontrada para atualização!'}), 404

        update_data = request.get_json()

        cliente.id = update_data.get('nome', cliente.id)
        cliente.login = update_data.get('duracao', cliente.login)
        cliente.senha = update_data.get('generos_id', cliente.senha)
        cliente.planos_id = update_data.get('lancamento', cliente.planos_id)
        cliente.email = update_data.get('email', cliente.email)

        db.session.commit()

        return jsonify({'message': 'Cliente atualizado com sucesso!'})
    elif request.method == 'DELETE':
        cliente = Cliente.query.get(cliente_id)

        if cliente is None:
            return jsonify({'message': 'Cliente não encontrado para deletar!'}), 404

        db.session.delete(cliente)
        db.session.commit()

        return jsonify({'message': 'Cliente deletado com sucesso!'}), 204


@app.route("/api/planos/", methods=['GET', 'POST'])
def planos():
    if request.method == 'GET':
        all_plano = Plano.query.all()

        return jsonify(plano_schemas.dump(all_plano))
    elif request.method == 'POST':
        new_plano = request.get_json()
        plano = Plano(new_plano['id'], new_plano['descricao'], new_plano['valor'], new_plano['limite'])

        db.session.add(plano)
        db.session.commit()

        return jsonify({'message': 'Plano criado com sucesso!'}), 201


@app.route("/api/planos/<int:plano_id>", methods=['GET', 'PATCH', 'DELETE'])
def planos_by_id(plano_id):
    if request.method == 'GET':
        plano = Plano.query.get(plano_id)

        if plano is None:
            return jsonify({'message': 'Plano não encontrado!'}), 404

        return jsonify(plano_schema.dump(plano))
    elif request.method == 'PATCH':
        plano = Plano.query.get(plano_id)

        if plano is None:
            return jsonify({'message': 'Plano não encontrado para atualização!'}), 404

        update_data = request.get_json()

        plano.id = update_data.get('id', plano.id)
        plano.descricao = update_data.get('descricao', plano.descricao)
        plano.valor = update_data.get('valor', plano.valor)
        plano.limite = update_data.get('limite', plano.limite)

        db.session.commit()

        return jsonify({'message': 'Plano atualizado com sucesso!'})
    elif request.method == 'DELETE':
        plano = Plano.query.get(plano_id)

        if plano is None:
            return jsonify({'message': 'Plano não encontrado para deletar!'}), 404

        db.session.delete(plano)
        db.session.commit()

        return jsonify({'message': 'Plano deletado com sucesso!'}), 204


@app.route("/api/pagamentos/", methods=['GET', 'POST'])
def pagamentos():
    if request.method == 'GET':
        all_pagamento = Pagamento.query.all()

        return jsonify(pagamento_schemas.dump(all_pagamento))
    elif request.method == 'POST':
        new_pagamento = request.get_json()
        pagamento = Pagamento(new_pagamento['id'])

        db.session.add(pagamento)
        db.session.commit()

        return jsonify({'message': 'Pagamento criado com sucesso!'}), 201


@app.route("/api/pagamentos/<int:pagamento_id>", methods=['GET', 'PATCH', 'DELETE'])
def pagamentos_by_id(pagamento_id):
    if request.method == 'GET':
        pagamento = Pagamento.query.get(pagamento_id)

        if pagamento is None:
            return jsonify({'message': 'Pagamento não encontrado!'}), 404

        return jsonify(pagamento_schema.dump(pagamento))
    elif request.method == 'PATCH':
        pagamento = Pagamento.query.get(pagamento_id)

        if pagamento is None:
            return jsonify({'message': 'Pagamento não encontrado para atualização!'}), 404

        update_data = request.get_json()

        pagamento.id = update_data.get('id', pagamento.id)

        db.session.commit()

        return jsonify({'message': 'Pagamento atualizado com sucesso!'})
    elif request.method == 'DELETE':
        pagamento = Pagamento.query.get(pagamento_id)

        if pagamento is None:
            return jsonify({'message': 'Pagamento não encontrado para deletar!'}), 404

        db.session.delete(pagamento)
        db.session.commit()

        return jsonify({'message': 'Pagamento deletado com sucesso!'}), 204


if __name__ == '__main__':
    app.run()
