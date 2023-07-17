from ast import Global
import sqlite3
from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox,QStackedWidget, QFileDialog,QTableWidgetItem
from PyQt5.QtSql import *
import sys

#no tocar esta funcion jeje
try:
    file=open('Bibliotkmdb.db') 
    print(file)
    file.close()
except FileNotFoundError:
    con = sqlite3.connect('Bibliotkmdb.db')
    curs = con.cursor()
    curs.execute("""CREATE TABLE IF NOT EXISTS Autores 
                 (idAutores INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Nombre TEXT (20) NOT NULL, Nombre2 TEXT (20) NOT NULL, Apellido TEXT (20) NOT NULL, Apellido2 TEXT (20) NOT NULL, Activo TEXT NOT NULL DEFAULT ACTIVO)""")
    con.commit()

    curs.execute("""CREATE TABLE IF NOT EXISTS Clientes 
                 (idClientes INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, Cedula TEXT (15) UNIQUE NOT NULL, Nombre TEXT (20) NOT NULL, Nombre2 TEXT (20) NOT NULL, Apellido TEXT (20) NOT NULL, Apellido2 TEXT (20) NOT NULL, Genero TEXT NOT NULL DEFAULT FEMENINO, fechaNa DATE NOT NULL, EstatusCliente TEXT (20) NOT NULL DEFAULT DESBLOQUEADO, Activo TEXT (9) NOT NULL DEFAULT ACTIVO)""")
    con.commit()

    curs.execute("""CREATE TABLE IF NOT EXISTS Libros 
                 (ISBM TEXT (13) PRIMARY KEY NOT NULL, Titulo TEXT (20) NOT NULL, F_Publicacion TEXT (10) NOT NULL, num_pags INTEGER NOT NULL, Editorial TEXT (35) NOT NULL, Ejemplares INTEGER NOT NULL, Genero TEXT (30) NOT NULL, Activo TEXT NOT NULL DEFAULT ACTIVO)""")
    con.commit()

    curs.execute("""CREATE TABLE IF NOT EXISTS Usuarios 
                 (idUsuario INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, Nombre TEXT (20) NOT NULL, Apellido TEXT (20) NOT NULL, Username TEXT (16) NOT NULL UNIQUE, Clave TEXT (40) NOT NULL, email TEXT (50) NOT NULL UNIQUE, Privilegios TEXT (15) NOT NULL, Verificado TEXT (5) NOT NULL DEFAULT NO, Activo TEXT (20) NOT NULL DEFAULT ACTIVO)""")
    con.commit()

    curs.execute("""CREATE TABLE IF NOT EXISTS Autores_Libros 
                 (ISBM TEXT (13) REFERENCES Libros (ISBM) NOT NULL, idAutores INTEGER REFERENCES Autores (idAutores) NOT NULL, ACTIVO TEXT DEFAULT ACTIVO NOT NULL)""")
    con.commit()

    curs.execute("""CREATE TABLE IF NOT EXISTS Prestamo 
                 (idPrestamo INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, idClientes INTEGER REFERENCES Clientes (idClientes) NOT NULL, idUsuario INTEGER REFERENCES Usuarios (idUsuario) NOT NULL, ISBM TEXT (13) REFERENCES Libros (ISBM) NOT NULL, F_d_sal TEXT NOT NULL, F_d_ent TEXT NOT NULL, F_d_enReal TEXT DEFAULT None, Activo TEXT NOT NULL DEFAULT ACTIVO)""")
    con.commit()

    # Insertamos usuario numero 1
    sql1 = "INSERT OR IGNORE INTO Usuarios(Nombre,Apellido,username,Clave,email,Privilegios,Verificado) VALUES (?,?,?,?,?,?,?)"
    param1 = ("Usuario", "Admin", "UserAdmin", "Bibliotk.2023", "bibliotksoftware@gmail.com", "ADMIN", "SI")

    curs.execute(sql1, param1)
    con.commit()

BDDbliotk='Bibliotkmdb.db'

def consulta(Consul, parametros=()):
    with sqlite3.connect(BDDbliotk) as cone:
        cursor= cone.cursor()
        resultado=cursor.execute(Consul,parametros)
        cone.commit()
    return resultado