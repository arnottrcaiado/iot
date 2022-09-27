# Faculdade SENAC
# Prof Arnott Ramos Caiado
# Exemplos de api
# dez 2020 - abr 2022

# -*- coding: UTF-8 -*-

from flask import Flask, render_template
from datetime import datetime, date
from flask import request
import json
import os

import pandas as pd
import time


######################################################################################## ic - diversas APIs
os.environ["TZ"] = "America/Recife"
time.tzset()

PATH_FILES = '/home/ads2napp/mysite/dados'
stat_lig1 = True # status de chave 1

api_key_post = "1A2b3C4E5f"
api_header_key = "ueyr123768565HGHgjhgHGHJghjghgHDFgdfdhgfklkjlkjuytty68"

app = Flask(__name__)
app.config['SECRET_KEY'] = '0123456789@'


# exemplos simples de end points
@app.route('/', methods=["GET","POST"])
def hello_world( ):
    chave ='ARNOTT'
#    chave=request.headers['Authorization-Token']
    if chave != 'ARNOTT':
        retorno ={'Erro#1':'erro de chave'}
    else:
        parametros = request.args
        retorno = {'Parametros': str(parametros.get('id'))}
    return json.dumps(retorno)
#    return render_template('index.html')


@app.route('/soma/<string:num1>/<string:num2>' )
def soma( num1, num2 ) :
    resultado = float(num1) + float(num2)
    return " A soma de " + num1 + " com " + num2 + " eh igual a " + str(resultado)

@app.route('/sub/<string:num1>/<string:num2>' )
def sub( num1, num2 ) :
    resultado = float(num1) - float(num2)
    return " A subtracao de " + num1 + " menos " + num2 + " eh igual a " + str(resultado)

# ---------------------------------------------------------------------------------------------------------

# end point para receber dados de IOT Arduino
@app.route('/datalog/<string:idthing>/<string:codigo>/<string:resposta>', methods=["GET","POST"])
def datalog( idthing, codigo, resposta ):
    data_atual = str(date.today())
    hora_atual = str(datetime.time(datetime.now()))
    hora_atual = hora_atual[0:5]
    idthing = idthing.lower()   # transforma a entrada em CAIXA BAIXA - isto facilita os testes

    # testar o codigo se valido
    caminho  = PATH_FILES+'/datalog.csv'
    ipuser = request.headers['X-Real-IP']
    arquivo = open(caminho,'a')
    linha = montaStr( idthing, str(ipuser), data_atual, hora_atual, resposta )
    arquivo.write( linha )
    arquivo.close()
    return json.dumps( {"Medida:"+str(resposta)},  ensure_ascii=False )

# end point para receber dados de IOT Arduino - armazenar apenas quando houver mudanças
@app.route('/datalogUltima/<string:idthing>/<string:codigo>/<string:resposta>', methods=["GET","POST"])
def datalog_Ultima( idthing, codigo, resposta ):
    data_atual = str(date.today())
    hora_atual = str(datetime.time(datetime.now()))
    hora_atual = hora_atual[0:5]
    idthing = idthing.lower()   # transforma a entrada em CAIXA BAIXA - isto facilita os testes

    # testar o codigo se valido
    caminho  = PATH_FILES+'/datalog.csv'
    caminho_log  = PATH_FILES+'/log.csv'

    ipuser = request.headers['X-Real-IP']
    linha = montaStr( idthing, str(ipuser), data_atual, hora_atual, resposta )

    if ( testa_Temp ( caminho, resposta ) ) : # testar se deve gravar o principal
        arquivo = open(caminho,'a')
        arquivo.write( linha )
        arquivo.close()

        arquivo = open(caminho_log,'a')
        arquivo.write( linha )
        arquivo.close()

        return json.dumps({"Medida":str(resposta)} ,  ensure_ascii=False )
    else :
        arquivo = open(caminho_log,'a')
        arquivo.write( linha )
        arquivo.close()
        return json.dumps({"Medida":"Sem alteração", "Valor":  str(resposta)},  ensure_ascii=False  )

# end point para receber dados de IOT Arduino - armazenar apenas quando houver mudanças
@app.route('/datalogpost', methods=["GET","POST"])
def datalog_post( ):

    api_chave = request.form['api_key']
    if api_chave != api_key_post or request.headers['Authorization-Token'] != api_header_key :
        return json.dumps({"Erro": "authenticação"},  ensure_ascii=False)

    idthing = request.form['id']
    codigo = request.form['chave']
    resposta = request.form['medida']
 #   lumi = request.form['luminosidade']

    data_atual = str(date.today())
    hora_atual = str(datetime.time(datetime.now()))
    hora_atual = hora_atual[0:5]
    idthing = idthing.lower()   # transforma a entrada em CAIXA BAIXA - isto facilita os testes

    # testar o codigo se valido
    caminho  = PATH_FILES+'/datalog.csv'
    caminho_log  = PATH_FILES+'/log.csv'

    ipuser = request.headers['X-Real-IP']
    linha = montaStr( idthing, str(ipuser), data_atual, hora_atual, resposta )

    if ( testa_Temp ( caminho, resposta ) ) : # testar se deve gravar o principal
        arquivo = open(caminho,'a')
        arquivo.write( linha )
        arquivo.close()

        arquivo = open(caminho_log,'a')
        arquivo.write( linha )
        arquivo.close()
        return json.dumps({"Medida": str(resposta)}, ensure_ascii=False)
    else :
        arquivo = open(caminho_log,'a')
        arquivo.write( linha )
        arquivo.close()
        return json.dumps ({"Medida":"Sem alteração", "Valor":  str(resposta)}, ensure_ascii=False)

@app.route('/datalog/numleituras')
def mostra() :
    arquivo = PATH_FILES+'/datalog.csv'
    dados = pd.read_csv( arquivo )
    leituras = len(dados)
    return json.dumps({"Mensagem":"Esta mensagem foi gerada pela api ads2napp.pythonanywhere.com/datalog/numleituras","Leituras": str(leituras) }, ensure_ascii=False)

# funcao para concatenar linha para arquivo csv
def montaStr( *args ) :
  st = ''
  t = len( args )
  for elemento in args :
    st = st + elemento
    t = t-1
    if t != 0 :
      st = st + ','
  st = st + "\n"
  return st

def testa_Temp ( caminho, temp ) :
    df=pd.read_csv(caminho)
    if df.loc[len(df)-1, 'temp'] == int(temp) :
        return False
    else :
        return True

@app.route('/datalog/temperatura')
def ultima_temp( ) :
    df=pd.read_csv( PATH_FILES+'/datalog.csv' )
    temp = df.loc[len(df)-1, 'temp']
    data = df.loc[len(df)-1, 'data']
    hora = df.loc[len(df)-1, 'hora']
    return json.dumps({'Temperatura': str(temp), 'Data': str(data), 'Hora': str(hora) }, ensure_ascii=False)


# #################################################
@app.route('/htm', methods=["GET","POST"])
def htm ():
    if request.method == 'GET':
        return render_template ( 'botoes.html' )
    if request.method == 'POST':
        op1=op2=op3=op4=op5=""
        if request.form.get("1"):
            op1=request.form.get("1")
        if request.form.get("2") :
            op2=request.form.get("2")
        if request.form.get("3"):
            op3=request.form.get("3")
        if request.form.get("4"):
            op4=request.form.get("4")
        if request.form.get("5"):
            op5=request.form.get("5")
        return op1+op2+op3+op4+op5

