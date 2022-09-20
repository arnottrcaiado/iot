#
# Faculdade SENAC PE
# Material de Apoio para Internet das Coisas
#
# Prof. Arnott Ramos Caiado
#
# ago/set 2022

# bibliotecas basicas
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Exemplo de um endpoit gerado automaticamente'

# exemplo de um endpoit para requisicoes basicas de consulta
@app.route('/get', methods=['GET'])
def getTest():
    cab = request.headers.get('Authorization-Token')
    return {"msg get": str(cab) }

# exemplo de um endpoit para requisicoes basicas POST
@app.route('/post', methods=['POST'])
def putTest():
    cab = request.headers.get('Authorization-Token')    # token que pode ser utilizado para validacao
    dados = request.get_json()
    sensor  = dados["sensor"]
    valor = dados["valor"]
    return {"sensor": str(sensor) , "valor": str(valor)}
