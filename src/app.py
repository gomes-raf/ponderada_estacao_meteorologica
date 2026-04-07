from flask import Flask
from flask import request, jsonify
from database import inserir_leitura

app = Flask(__name__)

@app.route('/leituras', methods=['POST'])
def criar():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400
    id_novo = inserir_leitura(
        dados['temperatura'],
        dados['umidade'],   
        dados.get('pressao')
    )
    return jsonify({'id': id_novo, 'status': 'criado'}), 201

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"