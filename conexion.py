from ast import Global
import sqlite3

BDDbliotk='Bibliotkmdb.db'

def consulta(Consul, parametros=()):
    with sqlite3.connect(BDDbliotk) as cone:
        cursor= cone.cursor()
        resultado=cursor.execute(Consul,parametros)
        cone.commit()
    return resultado
