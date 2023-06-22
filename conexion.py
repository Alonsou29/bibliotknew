from ast import Global
import sqlite3

BDDbliotk='Bibliotkmdb.db'

def consulta(Consul, parametros=()):
    with sqlite3.connect(BDDbliotk) as cone:
        cursor= cone.cursor()
        resultado=cursor.execute(Consul,parametros)
        cone.commit()
    return resultado

consul='SELECT Apellido2 FROM Clientes where idClientes=?'

param=(1,)
#print(consulta(consul).fetchall())

print(consulta(consul,param).fetchone())
print(consulta(consul,param).fetchmany())
print(consulta(consul,param).fetchall())