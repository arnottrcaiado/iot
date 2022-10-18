#
# Faculdade SENAC PE
# Material de Apoio para Internet das Coisas
#
# Prof. Arnott Ramos Caiado
# ago/set 2022
# bibliotecas basicas
#
from flask import Flask, request
import json
import os
import pandas as pd
import time
from datetime import datetime, date

######################################################################################## ic - diversas APIs
os.environ["TZ"] = "America/Recife"
time.tzset()

PATH_FILES = '/home/apiot/mysite/dados'

header_key = 'eFgHjukoli12Reatyghmaly76'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Exemplo de um endpoit gerado automaticamente'

# exemplo de um endpoit para requisicoes basicas de consulta
@app.route('/getJson', methods=['GET'])
def getJson():
    cab = request.headers.get('Authorization-Token')
    if validaHeader( cab ):
        return {"getJson header": "ok"}
    else :
        return {"getJson header": "erro"}

# ------------------------------------------------------------
# exemplo de um endpoit para consultar todo o volume de dados
@app.route('/getJsonAll', methods=['GET'])
def getJsonAll():
    df = pd.read_csv( PATH_FILES+'/log_dados.csv')
    result = df.to_json(orient="records")
    dados = json.loads(result)
    return json.dumps( dados)

# exemplo de um endpoit para consultar todo o volume de dados
@app.route('/getCount', methods=['GET'])
def getCount():
    df = pd.read_csv( PATH_FILES+'/log_dados.csv')
    linhas = len(df.index)
    return {"Linhas": str(linhas)}

# exemplo de um endpoit para requisicoes basicas POST. formato JSON
@app.route('/postJson', methods=['POST'])
def postJson():
    cab = request.headers.get('Authorization-Token')    # token que pode ser utilizado para validacao
    if validaHeader(cab) :
        dados = request.get_json()                          # recebe os dados em formato json
        sensor  = dados["sensor"]                           # identifica cada elemento do json de origem
        valor = dados["valor"]
        gravaDados ( sensor, valor )
        return {"status": str(sensor) , "valor": str(valor)}
    else :
        return {"status": "erro-header invalido"}
# end point para mostrar o uso da linha de comando com argumento
@app.route('/getLinha', methods=['GET'])
def getLinha():
    sensor = request.args.get('sensor')
    valor = request.args.get('valor')
    return {"Formato de linha http": "ok","sensor": str(sensor) , "valor": str(valor)}


# end point para receber dados no formato de form
@app.route('/postForm', methods=['GET','POST'])
def postForm():
    sensor = request.form['sensor']
    valor = request.form['valor']
    return {"Formato de form": "ok","sensor": str(sensor) , "valor": str(valor)}

# funcao para concatenar linha para arquivo csv
def montaStr( *args ) :
  st = ''
  for x in args :
    st += str(x)+','
  return st[0:-1]+'\n'

# grava dados
def gravaDados( sensor, valor ):
    data_atual = str(date.today())
    hora_atual = str(datetime.time(datetime.now()))
    hora_atual = hora_atual[0:5]
    linha = montaStr( sensor, data_atual, hora_atual, valor )
    arquivo = open(PATH_FILES+'/log_dados.csv','a')
    arquivo.write( linha )
    arquivo.close()
    return

# funcao para validar header
def validaHeader( cabecalho ):
    if cabecalho == header_key :
        return True
    else :
        return False