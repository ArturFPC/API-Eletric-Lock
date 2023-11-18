from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:c36Dehe-A6DAB23g2GE36A5fHbha2A2b@viaduct.proxy.rlwy.net:24823/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo da tabela Users
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, default=False)

# Modelo da tabela Access
class Access(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nfc = db.Column(db.String(255), nullable=False)

# Rota para adicionar um novo usuário
@app.route('/adicionar_usuario', methods=['POST'])
def adicionar_usuario():
    try:
        # Obtém os dados do corpo da requisição
        dados = request.json

        # Cria um novo usuário com base nos dados fornecidos
        novo_usuario = Users(
            name=dados['name'],
            email=dados['email'],
            password=dados['password'],
            admin=dados.get('admin', False)  # admin é opcional, assume False se não fornecido
        )

        # Adiciona o novo usuário ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({'mensagem': 'Usuário adicionado com sucesso!'})
    except Exception as e:
        return jsonify({'erro': str(e)})

#Rota para mostrar os usuários
@app.route('/mostrar_usuarios', methods=['GET'])
def mostrar_usuarios():
    try:
        # Obtém todos os usuários do banco de dados
        usuarios = Users.query.all()

        # Transforma os usuários em objetos JSON
        resultado = [
            {
                "id": usuario.id,
                "name": usuario.name,
                "email": usuario.email,
                "password": usuario.password,
                "admin": usuario.admin
            } for usuario in usuarios]

        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)})


# Rota para adicionar um novo acesso
@app.route('/adicionar_acesso', methods=['POST'])
def adicionar_acesso():
    try:
        # Obtém os dados do corpo da requisição
        dados = request.json

        # Cria um novo acesso com base nos dados fornecidos
        novo_acesso = Access(
            nfc=dados['nfc']
        )

        # Adiciona o novo acesso ao banco de dados
        db.session.add(novo_acesso)
        db.session.commit()

        return jsonify({'mensagem': 'Acesso adicionado com sucesso!'})
    except Exception as e:
        return jsonify({'erro': str(e)})

#Rota para mostrar os acessos
@app.route('/mostrar_acessos', methods=['GET'])
def mostrar_acessos():
    try:
        # Obtém todos os acessos do banco de dados
        acessos = Access.query.all()

        # Transforma os acessos em objetos JSON
        resultado = [
            {
                "id": acesso.id,
                "nfc": acesso.nfc
            } for acesso in acessos]

        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
