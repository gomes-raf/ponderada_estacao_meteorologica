from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import (
    init_db,
    inserir_leitura,
    listar_leituras,
    contar_leituras,
    buscar_leitura,
    atualizar_leitura,
    deletar_leitura,
)

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/historico')
def historico():
    leituras = listar_leituras(limite=10)
    return render_template('historico.html', leituras=leituras)

@app.route('/criar', methods=['POST'])
def criar_com_form():
    temperatura = request.form.get('temperatura')
    umidade = request.form.get('umidade')
    pressao = request.form.get('pressao') or None

    if not temperatura or not umidade:
        return redirect(url_for('index'))

    inserir_leitura(temperatura, umidade, pressao)
    return redirect(url_for('historico'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    leitura = buscar_leitura(id)
    if leitura is None:
        return redirect(url_for('historico'))

    if request.method == 'POST':
        dados = {
            'temperatura': request.form.get('temperatura'),
            'umidade': request.form.get('umidade'),
            'pressao': request.form.get('pressao') or None,
        }
        atualizar_leitura(id, dados)
        return redirect(url_for('historico'))

    return render_template('editar.html', leitura=leitura)

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar_leitura_form(id):
    leitura = buscar_leitura(id)
    if leitura is None:
        return redirect(url_for('historico'))
    deletar_leitura(id)
    return redirect(url_for('historico'))

@app.route('/leituras', methods=['GET'])
def listar_api():
    page = request.args.get('page', type=int)
    limit = request.args.get('limit', type=int)

    if page and limit:
        offset = (page - 1) * limit
        total = contar_leituras()
        leituras = listar_leituras(limite=limit, offset=offset)
        return jsonify({
            'leituras': leituras,
            'page': page,
            'limit': limit,
            'total': total,
        }), 200

    leituras = listar_leituras(limite=100)
    return jsonify(leituras), 200

@app.route('/leituras/<int:id>', methods=['GET'])
def obter_api(id):
    leitura = buscar_leitura(id)
    if leitura is None:
        return jsonify({'erro': 'Leitura não encontrada'}), 404
    return jsonify(leitura), 200

@app.route('/leituras', methods=['POST'])
def criar_api():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400

    if 'temperatura' not in dados or 'umidade' not in dados:
        return jsonify({'erro': 'Campos obrigatórios: temperatura, umidade'}), 400

    id_novo = inserir_leitura(
        dados['temperatura'],
        dados['umidade'],
        dados.get('pressao'),
    )
    return jsonify({'id': id_novo, 'status': 'criado'}), 201

@app.route('/leituras/<int:id>', methods=['PUT', 'PATCH'])
def atualizar_api(id):
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'JSON inválido'}), 400

    leitura = buscar_leitura(id)
    if leitura is None:
        return jsonify({'erro': 'Leitura não encontrada'}), 404

    if 'temperatura' not in dados or 'umidade' not in dados:
        return jsonify({'erro': 'Campos obrigatórios: temperatura, umidade'}), 400

    leitura_atualizada = atualizar_leitura(id, dados)
    return jsonify(leitura_atualizada), 200

@app.route('/leituras/<int:id>', methods=['DELETE'])
def deletar_api(id):
    leitura = buscar_leitura(id)
    if leitura is None:
        return jsonify({'erro': 'Leitura não encontrada'}), 404

    deletar_leitura(id)
    return jsonify({'status': 'deletado'}), 200



if __name__ == '__main__':
    app.run(debug=True)