from ast import Global
import MySQLdb

def conec(consul,param=()):
    try:
        conec=MySQLdb.connect(host='localhost',user='root',password="",database='mydb')
        print("conexion realizada")

        cur=conec.cursor()

        q1=cur.execute(consul,param)
        resultado=cur.fetchall()
        conec.commit()
        conec.close()

        return resultado
    except Exception as xtr:
        print(xtr)
