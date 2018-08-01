# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from flask_jsonpify import jsonify

db_connect = create_engine('sqlite:///conplei.db')
    
def upsertParticipantes(firstName, lastName, gender, country, state, city, tribo, vaiconplei, maisalguemvai, respostainicial, userid):
    try:
        conn = db_connect.connect()
        
        query = conn.execute("select count(1) from participantes where userid = '{0}'".format(userid))
        count = int(str(query.cursor.fetchall()[0][0]))
        
        if gender == 'male':
            gender = 'M'
        else:
            gender = 'F'
        
        if 'Não' in respostainicial:
            respostainicial = 'Não'
        else:
            respostainicial = ''
        
        if count == 0:  
            comando="""INSERT INTO participantes (
                              userid,
                              primeironome,
                              ultimonome,
                              genero,
                              pais,
                              estado,
                              cidade,
                              tribo,
                              datacadastro,
                              dataalteracao,
                              vaiconplei,
                              maisalguemvai,
                              naoquerresponder
                          )
                          VALUES (
                              '{0}',
                              '{1}',
                              '{2}',
                              '{3}',
                              '{4}',
                              '{5}',
                              '{6}',
                              '{7}',
                              date('now'),
                              date('now'),
                              '{8}',
                              '{9}',
                              '{10}'
                          );""".format(userid,
                                       firstName,
                                       lastName,
                                       gender,
                                       country,
                                       state,
                                       city,
                                       tribo,
                                       vaiconplei,
                                       maisalguemvai,
                                       respostainicial)
            print("Comando:", comando)
            conn.execute(comando)
        else:
            
            comando = """UPDATE participantes set
                              primeironome = '{1}',
                              ultimonome = '{2}',
                              genero = '{3}',
                              pais = '{4}',
                              estado = '{5}',
                              cidade = '{6}',
                              tribo = '{7}',
                              dataalteracao = date('now'),
                              vaiconplei = '{8}',
                              maisalguemvai = '{9}',
                              naoquerresponder = '{10}'
                            WHERE userid = '{0}';""".format(userid,
                                       firstName,
                                       lastName,
                                       gender,
                                       country,
                                       state,
                                       city,
                                       tribo,
                                       vaiconplei,
                                       maisalguemvai,
                                       respostainicial)
            print("Comando:", comando)
            conn.execute(comando)
            
        conn.close()
            
        return True
    except Exception as e:
        print('[upsertParticipantes] Erro:', e)
        return False
    
def upsertIndicados(userid, nome, telefone):
    try:
        conn = db_connect.connect()
        
        query = conn.execute("select count(1) from indicados where userid = '{0}' and nome = '{1}'".format(userid, nome))
        count = int(str(query.cursor.fetchall()[0][0]))
        
        if count == 0:  
            comando="""INSERT INTO indicados (
                              userid,
                              nome,
                              telefone
                          )
                          VALUES (
                              '{0}',
                              '{1}',
                              '{2}'
                          );""".format(userid,
                                       nome,
                                       telefone)
            print("Comando:", comando)
            conn.execute(comando)
        else:
            
            comando = """UPDATE indicados set
                              telefone = '{2}'
                            WHERE userid = '{0}' and nome = '{1}';""".format(userid,
                                       nome,
                                       telefone)
            print("Comando:", comando)
            conn.execute(comando)
            
        conn.close()
            
        return True
    except Exception as e:
        print('[upsertIndicados] Erro:', e)
        return False

def getAllParticipantes():
    conn = db_connect.connect()
    
    try:
        query = conn.execute("select * from participantes") 
        return jsonify({'participantes': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor.fetchall()]})
    except Exception as e:
        print('[getAllParticipantes] Erro:', e)
        return {}

def getAllIndicados():
    conn = db_connect.connect()
    
    try:
        query = conn.execute("select * from indicados") 
        return jsonify({'indicados': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor.fetchall()]})
    except Exception as e:
        print('[getAllIndicados] Erro:', e)
        return {}