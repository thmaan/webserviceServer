from flask import Flask
from flask import current_app, jsonify, make_response, redirect, request, url_for, abort
from flask_httpauth import HTTPBasicAuth
from datetime import datetime

auth = HTTPBasicAuth()

app = Flask(__name__)

dados = [
    {
        'id':1,
        'temperatura':30,
        'umidade':5,
        'luminosidade': 3.5,
        'datahora':'10/02/2021 02:45:00 PM'
    },
    {
        'id':2,
        'temperatura':22,
        'umidade':2,
        'luminosidade': 2.2,
        'datahora':'10/02/2021 02:46:00 PM'
    },
    {
        'id':3,
        'temperatura':22,
        'umidade':2,
        'luminosidade': 2.2,
        'datahora':'10/02/2021 02:47:00 PM'
    },
    {
        'id':4,
        'temperatura':22,
        'umidade':2,
        'luminosidade': 2.2,
        'datahora':'10/02/2021 02:48:00 PM'
    }
]

# curl -i http://127.0.0.1:5000/dados
#
@app.route('/dados', methods=['GET'])
def obtem_dados():
    data=len(dados) - 1
    data = {'dados': dados[data]}
    return jsonify(data), 200

@app.route('/dados-filtrados', methods=['POST'])
def get_dados_by_id():
    if not request.json or not 'id' in request.json:
        abort(400)
    data = request.json.get('id')
    data = int(data) -1
    print(data)
    return jsonify({'dados': dados[data]}), 200

@app.route('/dados-filtrados-datahora', methods=['POST'])
def get_dados_by_datahora():
    if not request.json or not 'datahora' in request.json:
        abort(400)
    data = request.json.get('datahora')
    for itens in dados:
        print(data)
        print("")
        print(itens['datahora'])
        if itens['datahora'] == data:
            i = itens['id']
            return jsonify({'dados': dados[i-1]}), 200
    return jsonify({'dados': dados[0]}), 200

# curl -i -H "Content-Type: application/json" -X POST -d '{"temperatura":"10","umidade":"4","luminosidade":"15"}' http://127.0.0.1:5000/livros
#
@app.route('/inserir-dados', methods=['POST'])
def inserir_dados():
    if not request.json or not 'id' in request.json:
        abort(400)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    dado = {
        'id': dados[-1]['id'] + 1,
        'temperatura': request.json.get('temperatura'),
        'umidade': request.json.get('umidade'),
        'luminosidade': request.json.get('luminosidade'),
        'datahora': dt_string
    }
    dados.append(dado)
    return jsonify({'dados': dados}), 200

# curl -i -X DELETE http://127.0.0.1:5000/dados/2
#
@app.route('/dados/<int:idDado>', methods=['DELETE'])
def excluir_dado(idDado):
    resultado = [resultado for resultado in dados if resultado['id'] == idDado]
    if len(resultado) == 0:
        abort(404)
    dados.remove(resultado[0])
    return jsonify({'resultado': True})

# curl -i -H "Content-Type: application/json" -X PUT -d '{"temperatura":"15"} http://127.0.0.1:5000/livros/2
#
@app.route('/dados/<int:idDado>', methods=['PUT'])
def atualizar_dado(idDado):
    resultado = [resultado for resultado in dados if resultado['id'] == idDado]
    if len(resultado) == 0:
        abort(404)
    if not request.json:
        abort(400)
    resultado[0]['temperatura'] = request.json.get('temperatura', resultado[0]['temperatura'])
    resultado[0]['umidade'] = request.json.get('umidade', resultado[0]['umidade'])
    resultado[0]['luminosidade'] = request.json.get('luminosidade', resultado[0]['luminosidade'])
    return jsonify({'dados': resultado[0]}), 200

if __name__ == "__main__":
    print('Servidor executando...')
    app.run(debug=True)
