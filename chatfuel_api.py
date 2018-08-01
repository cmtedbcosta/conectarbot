#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 17:04:04 2018

@author: daniel
"""

import os
from flask import Flask, request
from furl import furl
from Models import upsertParticipantes, getAllParticipantes, upsertIndicados, getAllIndicados
app = Flask(__name__)

@app.route('/', methods=['GET'])
def webhook():
    
    f = furl(request.url) 
    
    print ('Primeiro Nome:', f.args['first name'])
    print ('Ultimo Nome:', f.args['last name'])
    print ('Genero:', f.args['gender'])
    
    print ('Pais:', f.args['country'])
    print ('Estado:', f.args['state'])
    print ('Cidade:', f.args['city'])
    
    print ('Tribo:', f.args['Tribo'])
    print ('Vai ao Conplei:', f.args['ParticiparConplei'])
    print ('Mais alguém da tribo vai:', f.args['MaisAlguemTriboVai'])
    print ('Indicado:', f.args['Indicado'])
    print ('Telefone do Indicado:', f.args['TelefoneIndicado'])
    
    print ('Chatfuel user id:', f.args['chatfuel user id'])
    print ('Messenger user id:', f.args['messenger user id'])
    
    print ('Reposta Inicial:', f.args['RespostaInicial'])
    print ('Está no Conplei:', f.args['EstaConplei'])
    
    ret = upsertParticipantes(f.args['first name'],
                              f.args['last name'],
                              f.args['gender'],
                              f.args['country'],
                              f.args['state'],
                              f.args['city'],
                              f.args['Tribo'],
                              f.args['ParticiparConplei'],
                              f.args['MaisAlguemTriboVai'],
                              f.args['RespostaInicial'],
                              f.args['chatfuel user id'])
    
    if (ret):
        upsertIndicados(f.args['chatfuel user id'], f.args['Indicado'], f.args['TelefoneIndicado'])
        print('Upsert executado com sucesso.')
    else:
        print('Erro ao executar upsert.')
    
    return "OK", 200

@app.route('/participantes', methods=['GET'])
def getParticipantes():
    participantes = getAllParticipantes()
    return participantes, 200

@app.route('/indicados', methods=['GET'])
def getIndicados():
    indicados = getAllIndicados()
    return indicados, 200

if __name__ == '__main__':
     port = int(os.environ.get("PORT", 5000))
     app.run(host='0.0.0.0', port=port)