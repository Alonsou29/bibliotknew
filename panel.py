import sys
import os
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import (QMainWindow,QApplication,QMessageBox,QStackedWidget, QFileDialog,QTableWidgetItem,QAbstractItemView, QInputDialog)
from PyQt5.QtSql import *
from conexion import consulta
from PyQt5.QtSql import *
import re
import shutil
import webbrowser
import matplotlib.pyplot as plt
import pdfkit
import jinja2
from datetime import *
from email.message import EmailMessage
import ssl
import smtplib
import random
from autores import Autores
from clientes import Clientes
from libros import Libros


class PanelControl(QMainWindow):

    # Constructor del frame
    def __init__(self,userid):
        super().__init__()
        # Carga Panel de cotrol
        self.panel = uic.loadUi("frames\panel.ui",self)
 
        # Establece titulo de la ventana
        self.panel.setWindowTitle("Bibliotk")
        self.panel.setWindowIcon(QtGui.QIcon('logo.png'))
        # Establece el tamaño de la ventana y hace que no puedas cambiar su tamaño
        self.panel.setFixedSize(800, 600) # (Ancho, Alto)

        # Variable que usaremos para codigos de verificacion en correos
        self.verifCode = 0

        # Variable que usaremos para almacenar el id del usuario
        self.usuario = userid

        self.perfilDatos(self.usuario)

        # Visualiza pantalla de inicio
        self.panel.stackedWidget.setCurrentIndex(0)

        # Triggers de las funciones del menubar
        self.panel.actionMostrarI.triggered.connect(self.inicioIr) # Inicio
        self.panel.actionMostrarP.triggered.connect(self.perfilIr) # Perfil
        self.panel.actionRegistrosC.triggered.connect(self.clientesIr) # Clientes
        self.panel.actionRegistrosL.triggered.connect(self.librosIr) # Libros
        self.panel.actionRegistrosA.triggered.connect(self.autoresIr) # Autores
        self.panel.actionResgistrosP.triggered.connect(self.prestamosIr) # Prestamos
        self.panel.actionMostrarE.triggered.connect(self.estadisticasIr) # Estadisticas
        self.panel.actionMostrarR.triggered.connect(self.reportesIr) # Reportes
        self.panel.actionRespaldar.triggered.connect(self.respaldarBDD) # Mantenimiento: Respaldar BDD
        self.panel.actionRestaurar.triggered.connect(self.restaurarBDD) # Mantenimiento: Restaurar BDD
        self.panel.actionResgistrosU.triggered.connect(self.usuariosIr) # Usuarios
        self.panel.actionAcerca_de.triggered.connect(self.acercaDe) # Ayuda: Acerca de
        self.panel.actionManual_de_Usuario.triggered.connect(self.abrirManual) # Ayuda: Manual de usuario



        #FUNCIONES DE LOS BOTONES

            #Funcion Buscar
        self.panel.BuscarA.clicked.connect(lambda:self.buscarAutores())
        self.panel.BuscarL.clicked.connect(lambda:self.buscarLibros())
        self.panel.BuscarC.clicked.connect(lambda:self.buscarClientes())
        self.panel.BuscarU.clicked.connect(lambda:self.buscarUsuarios())

            #Eliminar Autores
        EliminarAsql="UPDATE Autores SET Activo = 'INACTIVO' WHERE idAutores=?"
        self.panel.EliminarA.clicked.connect(lambda:self.eliminarFila(EliminarAsql))
        self.panel.RefrescarA.clicked.connect(lambda:self.datosAutores())

            #Eliminar Libros
        EliminarLsql="UPDATE Libros SET Activo = 'INACTIVO' WHERE ISBM=?"
        self.panel.EliminarL.clicked.connect(lambda:self.eliminarFila(EliminarLsql))
        self.panel.RefrescarL.clicked.connect(lambda:self.datosLibros())

            #Eliminar Clientes
        EliminarCsql="UPDATE Clientes SET Activo = 'INACTIVO' WHERE Cedula=?"
        self.panel.EliminarC.clicked.connect(lambda:self.eliminarFila(EliminarCsql))
        self.panel.RefrescarC.clicked.connect(lambda:self.datosClientes())

            #Eliminar Usuarios
        EliminarUsql="UPDATE Usuarios SET Activo = 'INACTIVO' WHERE idUsuario=?"
        self.panel.EliminarU.clicked.connect(lambda:self.eliminarFila(EliminarUsql))
        self.panel.RefrescarU.clicked.connect(lambda:self.datosUsuarios())

            #Eliminar Prestamos
        EliminarPsql="UPDATE Prestamo SET Activo = 'INACTIVO' WHERE idPrestamo=?"
        self.panel.EliminarP.clicked.connect(lambda:self.eliminarFila(EliminarPsql))
        self.panel.RefrescarP.clicked.connect(lambda:self.datosPrestamo())

            #Modifica Autores
        self.panel.tabla_Autores.clicked.connect(lambda:self.verdatoAutores())
        self.panel.ModificarA.clicked.connect(lambda:self.ModificarAutores())

            #Modificar Libros
        self.panel.tabla_Libros.clicked.connect(lambda:self.verdatoLibros())
        self.panel.ModificarL.clicked.connect(lambda:self.ModificarLibros())

            #Modificar Clientes
        self.panel.tabla_Clientes.clicked.connect(lambda:self.verdatoClientes())
        self.panel.ModificarC.clicked.connect(lambda:self.ModificarClientes())

            #Modificar Usuarios
        self.panel.tabla_Usuarios.clicked.connect(lambda:self.verdatoUsuarios())
        self.panel.ModificarU.clicked.connect(lambda:self.ModificarUsuarios())

            #Modificar Prestamos
        self.panel.tabla_Prestamos.clicked.connect(lambda:self.verdatoPrestamos())

            #Insertar datos
        self.panel.NuevoA.clicked.connect(lambda:self.InsertarAutores())
        self.panel.NuevoU.clicked.connect(lambda:self.InsertarUsuarios())
        self.panel.NuevoC.clicked.connect(lambda:self.InsertarClientes())
        self.panel.NuevoL.clicked.connect(lambda:self.InsertarLibros())

            # Generar Reportes
        self.panel.Generar_Reportes_E.clicked.connect(lambda:self.reporteEst()) # Estadisticas
        self.panel.Generar_Reportes_P.clicked.connect(lambda:self.reportePres()) # Prestamos

            # Seleccionar Autores de libros
        self.panel.Busca_autores_libros.clicked.connect(lambda:self.seleccionarAutores())
        
            # Seleccionar Cliente del prestamo
        self.panel.Busca_cliente_prestamo.clicked.connect(lambda:self.seleccionarClientes())

            # Seleccionar Libro del prestamo
        self.panel.Busca_libro_prestamo.clicked.connect(lambda:self.seleccionarLibros())


    def seleccionarAutores(self):
        self.selecA = Autores()
        #self.selecA.
        self.selecA.show()

    def seleccionarClientes(self):
        self.selecC = Clientes()
        self.tablaC2=self.selecC.tabla_Clientes2
        sql="SELECT idClientes,Cedula,Nombre,Nombre2,Apellido,Apellido2,Genero,fechaNa,EstatusCliente FROM Clientes"
        res= consulta(sql).fetchall()
        colum=len(res)
        self.tablaC2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget = self.selecC.tabla_Clientes2
        self.tableWidget.setRowCount(colum)
        sql3="SELECT Activo FROM Clientes"
        eliminar=consulta(sql3).fetchall()
        count=0
        tablerow=0

        for i in eliminar:
            print(i)
            Verf=i
            Eliminar1=str(Verf)
            Eliminar2=re.sub(",","",Eliminar1)
            Eliminar3=re.sub("'","",Eliminar2)
            Eliminar4=re.sub("()","",Eliminar3)
            vddfi =re.sub("[()]","",Eliminar4)
            print(vddfi)
            if vddfi!="ACTIVO":
                self.tabla.setRowHidden(count, True)
            else:
                for row in res:
                    self.id= row[0]
                    self.tablaC2.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                    self.tablaC2.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                    self.tablaC2.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
                    self.tablaC2.setItem(tablerow,3,QTableWidgetItem(str(row[3])))
                    self.tablaC2.setItem(tablerow,4,QTableWidgetItem(str(row[4])))
                    self.tablaC2.setItem(tablerow,5,QTableWidgetItem(str(row[5])))
                    self.tablaC2.setItem(tablerow,6,QTableWidgetItem(str(row[6])))
                    self.tablaC2.setItem(tablerow,7,QTableWidgetItem(str(row[7])))
                    self.tablaC2.setItem(tablerow,8,QTableWidgetItem(str(row[8])))
                    tablerow+=1
            count+=1
        self.selecC.seleccionar.clicked.connect(lambda:self.btn_selectC())
        self.selecC.show()

    def seleccionarLibros(self):
        self.selecL = Libros()
        self.tablaL2=self.selecL.tabla_Libros2
        sql2="SELECT ISBM,Titulo,F_Publicacion,num_pags,Editorial,Genero,Ejemplares FROM Libros"
        res= consulta(sql2).fetchall()
        self.tablaL2.setSelectionBehavior(QAbstractItemView.SelectRows)
        colum=len(res[0])
        sql3="SELECT Activo FROM Libros"
        eliminar=consulta(sql3).fetchone()
        self.tableWidget = self.selecL.tabla_Libros2
        self.tableWidget.setRowCount(colum)
        tablerow=0
        count=0
        
        for i in eliminar:
            Verf=i
            Eliminar1=str(Verf)
            Eliminar2=re.sub(",","",Eliminar1)
            Eliminar3=re.sub("'","",Eliminar2)
            Eliminar4=re.sub("()","",Eliminar3)
            vddfi =re.sub("[()]","",Eliminar4)
            print(i)
            print(vddfi)
            for row in res:
                if vddfi!="ACTIVO":
                    self.tablaL2.setRowHidden(count, True)
                else:
                    self.id= row[0]
                    self.tablaL2.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                    self.tablaL2.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                    self.tablaL2.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
                    self.tablaL2.setItem(tablerow,3,QTableWidgetItem(str(row[3])))
                    self.tablaL2.setItem(tablerow,4,QTableWidgetItem(str(row[4])))
                    self.tablaL2.setItem(tablerow,5,QTableWidgetItem(str(row[5])))
                    self.tablaL2.setItem(tablerow,6,QTableWidgetItem(str(row[6])))
                    tablerow+=1
                count+=1
        self.selecL.seleccionar.clicked.connect(lambda:self.btn_selectL())
        self.selecL.show()
        

    def btn_selectL(self):
        filaSeleccionada = self.tablaL2.selectedItems()
        if filaSeleccionada:
            self.panel.buscar_Libro.setText(filaSeleccionada[0].text())
        self.selecL.close()
    
    def btn_selectC(self):
        filaSeleccionada = self.tablaC2.selectedItems()
        if filaSeleccionada:
            self.panel.buscar_Cliente.setText(filaSeleccionada[0].text())
        self.selecC.close()


    def perfilDatos(self,userid):
        sql="SELECT Nombre,Apellido,Username,Clave,email FROM Usuarios WHERE idUsuario=?"
        param=(userid,)
        dato=consulta(sql,param).fetchall()
        for i in dato:
            self.panel.NombrePerfil.setText(i[0])
            self.panel.ApellidoPerfil.setText(i[1])
            self.panel.UsernamePerfil.setText(i[2])
            self.panel.EmailPerfil.setText(i[4])


    def privilegios(self):
        # Verificamos si el usuario es admin o no
        sql="SELECT Privilegios FROM Usuarios WHERE idUsuario=? AND Activo=?"
        param=(self.usuario,"ACTIVO") 
        dato=consulta(sql,param).fetchone()
        Eliminar1=str(dato)
        Eliminar2=re.sub(",","",Eliminar1)
        Eliminar3=re.sub("'","",Eliminar2)
        Eliminar4=re.sub("()","",Eliminar3)
        privilegio =re.sub("[()]","",Eliminar4)

        if privilegio !="ADMIN":
            # Oculta Mantenimiento
            self.panel.actionRespaldar.setVisible(False)
            self.panel.actionRestaurar.setVisible(False)
            self.panel.menuMantenimiento.setTitle("")

            # Oculta Usuarios
            self.panel.actionResgistrosU.setVisible(False)
            self.panel.menuUsuarios.setTitle("")

    # Funciones del menubar
    def inicioIr(self):
        # Camabia la pantalla a la seleccionada
        self.panel.stackedWidget.setCurrentIndex(0)

    def perfilIr(self):
        self.panel.stackedWidget.setCurrentIndex(1)
        # Comprobamos si el usuario está ferificado o no
        sql = "SELECT Verificado FROM Usuarios WHERE idUsuario=?"
        param=(self.usuario,)
        dato = consulta(sql,param).fetchone()
        Eliminar1=str(dato)
        Eliminar2=re.sub(",","",Eliminar1)
        Eliminar3=re.sub("'","",Eliminar2)
        Eliminar4=re.sub("()","",Eliminar3)
        verificacion =re.sub("[()]","",Eliminar4)

        # Si el usuario no esta verificado hacemos la verificacion
        if verificacion == "NO":
            self.verificarCorreo()

    def verificarCorreo(self):
        self.verifCode = random.randint(100000, 999999)

        sql = "SELECT email FROM Usuarios WHERE idUsuario=?"
        param=(self.usuario,)
        dato = consulta(sql,param).fetchone()
        Eliminar1=str(dato)
        Eliminar2=re.sub(",","",Eliminar1)
        Eliminar3=re.sub("'","",Eliminar2)
        Eliminar4=re.sub("()","",Eliminar3)
        emailUser =re.sub("[()]","",Eliminar4)

        # Enviamos codigo de verificacion por correo
        # El asunto y el cuerpo del correo
        asuntoCorreo = "Verificación de Email"
        cuerpoCorreo = """Estimado usuario, gracias por usar nuestros servicios. 
        
        Para verificar su correo ingrese en su perfil el siguiente código: 
        
        Código de verificación: """ + str(self.verifCode) + """

        Bibliotk Software"""
        # print(str(self.verifCode))
        self.enviarCorreo(emailUser, asuntoCorreo, cuerpoCorreo)
        
        numeroCorrecto = False

        while not numeroCorrecto:
            numero, estado = QInputDialog().getText(self, "Verificar Correo", "Para verificar su correo electrónico le hemos enviado\nun código de verificación, ingrese el código aquí: ")
            if estado:
                if numero.isdigit():
                    if numero == str(self.verifCode):
                        # En bdd cambiar verificado a SI
                        sql="UPDATE Usuarios SET Verificado=? WHERE email=?"
                        param=("SI", emailUser)
                        consulta(sql,param)

                        QMessageBox.information(self, "Aviso", "Correo verificado", QMessageBox.Ok)
                        numeroCorrecto = True
                    else:
                        QMessageBox.critical(self, "Error", "Código incorrecto")
                else:
                    QMessageBox.critical(self, "Error", "Código inválido")
            else:
                numeroCorrecto = True
    

    def enviarCorreo(self, email_receptor, asunto, cuerpo):
        email_emisor = "bibliotksoftware@gmail.com"
        email_clave = "lhztgqvmlivfklkt"

        # Preparamos el correo que enviaremos
        em = EmailMessage()
        em["From"] = email_emisor
        em["To"] = email_receptor
        em["Subject"] = asunto
        em.set_content(cuerpo)
        contexto = ssl.create_default_context()

        # "smtp.gmail.com" es el tipo de correo del emisor
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as smtp:
            # Iniciamos sesion en bibliotksoftware@gmail.com
            smtp.login(email_emisor, email_clave)

            # Enviamos email
            smtp.sendmail(email_emisor, email_receptor, em.as_string())

    def clientesIr(self):
        self.panel.stackedWidget.setCurrentIndex(2)
        self.datosClientes()
        
    def librosIr(self):
        self.panel.stackedWidget.setCurrentIndex(3)
        self.datosLibros()
   

   #Muestra los datos de cliente
    def datosClientes(self):
        self.tabla=self.panel.tabla_Clientes
        sql="SELECT idClientes,Cedula,Nombre,Nombre2,Apellido,Apellido2,Genero,fechaNa,EstatusCliente FROM Clientes"
        res= consulta(sql).fetchall()
        colum=len(res)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget = self.panel.tabla_Clientes
        self.tableWidget.setRowCount(colum)
        sql3="SELECT Activo FROM Clientes"
        now=self.panel.FechaNC.date()
        fecha=now.toPyDate()
        f1_str = fecha.strftime('%d/%m/%Y')
        eliminar=consulta(sql3).fetchall()
        count=0
        tablerow=0
        self.panel.CedulaC.clear()
        self.panel.NombreC.clear()
        self.panel.Nombre2C.clear()
        self.panel.ApellidoC.clear()
        self.panel.Apellido2C.clear()
        self.panel.ComboGC.setCurrentIndex(0)
        self.panel.ComboEC.setCurrentIndex(0)

        for i in eliminar:
            print(i)
            Verf=i
            Eliminar1=str(Verf)
            Eliminar2=re.sub(",","",Eliminar1)
            Eliminar3=re.sub("'","",Eliminar2)
            Eliminar4=re.sub("()","",Eliminar3)
            vddfi =re.sub("[()]","",Eliminar4)
            print(vddfi)
            if vddfi!="ACTIVO":
                self.tabla.setRowHidden(count, True)
            else:
                for row in res:
                    self.id= row[0]
                    self.tabla.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                    self.tabla.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                    self.tabla.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
                    self.tabla.setItem(tablerow,3,QTableWidgetItem(str(row[3])))
                    self.tabla.setItem(tablerow,4,QTableWidgetItem(str(row[4])))
                    self.tabla.setItem(tablerow,5,QTableWidgetItem(str(row[5])))
                    self.tabla.setItem(tablerow,6,QTableWidgetItem(str(row[6])))
                    self.tabla.setItem(tablerow,7,QTableWidgetItem(str(row[7])))
                    self.tabla.setItem(tablerow,8,QTableWidgetItem(str(row[8])))
                    tablerow+=1
            count+=1

    #Muestra los datos de usuarios
    def datosUsuarios(self):
        self.tabla=self.panel.tabla_Usuarios
        sql2="SELECT idUsuario,Nombre,Apellido,Username,Clave,email,Privilegios FROM Usuarios"
        res= consulta(sql2).fetchall()
        colum=len(res)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget = self.panel.tabla_Usuarios
        self.tableWidget.setRowCount(colum)
        sql3="SELECT Activo FROM Usuarios"
        eliminar=consulta(sql3).fetchone()
        count=0
        tablerow=0
        self.panel.NombreU.clear()
        self.panel.ApellidoU.clear()
        self.panel.UsernameU.clear()
        self.panel.ClaveU.clear()
        self.panel.EmailU.clear()
        self.panel.ComboGC_2.setCurrentIndex(0)
        for i in eliminar:
            Verf=i
            Eliminar1=str(Verf)
            Eliminar2=re.sub(",","",Eliminar1)
            Eliminar3=re.sub("'","",Eliminar2)
            Eliminar4=re.sub("()","",Eliminar3)
            vddfi =re.sub("[()]","",Eliminar4)
            print(i)
            print(vddfi)
            if vddfi!="ACTIVO":
                self.tabla.setRowHidden(count, True)
            else:
                for row in res:
                    self.id= row[0]
                    self.tabla.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                    self.tabla.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                    self.tabla.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
                    self.tabla.setItem(tablerow,3,QTableWidgetItem(str(row[3])))
                    self.tabla.setItem(tablerow,4,QTableWidgetItem(str(row[4])))
                    self.tabla.setItem(tablerow,5,QTableWidgetItem(str(row[5])))
                    self.tabla.setItem(tablerow,6,QTableWidgetItem(str(row[6])))
                    tablerow+=1
            count+=1

    #Muestra los datos de Autores
    def datosAutores(self):
        self.tabla=self.panel.tabla_Autores
        sql2="SELECT idAutores,Nombre,Nombre2,Apellido,Apellido2 FROM Autores"
        res= consulta(sql2).fetchall()
        colum=len(res)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget = self.panel.tabla_Autores
        self.tableWidget.setRowCount(colum)
        tablerow=0
        sql3="SELECT Activo FROM Autores"
        eliminar=consulta(sql3).fetchall()
        count=0
        self.panel.NombreA.clear()
        self.panel.Nombre2A.clear()
        self.panel.ApellidoA.clear()
        self.panel.Apellido2A.clear()
        
        for i in eliminar:
            Verf=i
            Eliminar1=str(Verf)
            Eliminar2=re.sub(",","",Eliminar1)
            Eliminar3=re.sub("'","",Eliminar2)
            Eliminar4=re.sub("()","",Eliminar3)
            vddfi =re.sub("[()]","",Eliminar4)

            if vddfi!="ACTIVO":
                self.tabla.setRowHidden(count, True)
            else:
                for row in res:
                    self.id= row[0]
                    self.tabla.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                    self.tabla.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                    self.tabla.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
                    self.tabla.setItem(tablerow,3,QTableWidgetItem(str(row[3])))
                    self.tabla.setItem(tablerow,4,QTableWidgetItem(str(row[4])))
                    tablerow+=1 
            count+=1

    #Muestra los datos de libros
    def datosLibros(self):
        self.tabla=self.panel.tabla_Libros
        sql2="SELECT ISBM,Titulo,F_Publicacion,num_pags,Editorial,Genero,Ejemplares FROM Libros"
        res= consulta(sql2).fetchall()
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        colum=len(res[0])
        sql3="SELECT Activo FROM Libros"
        eliminar=consulta(sql3).fetchone()
        self.tableWidget = self.panel.tabla_Libros
        self.tableWidget.setRowCount(colum)
        tablerow=0
        count=0
        self.panel.ISBML.clear()
        self.panel.TituloL.clear()
        self.panel.FechaPL.clear()
        self.panel.Nropags.clear()
        self.panel.EditorialL.clear()
        self.panel.EjemplaresL.clear()
        self.panel.GeneroL.clear()

        for i in eliminar:
            Verf=i
            Eliminar1=str(Verf)
            Eliminar2=re.sub(",","",Eliminar1)
            Eliminar3=re.sub("'","",Eliminar2)
            Eliminar4=re.sub("()","",Eliminar3)
            vddfi =re.sub("[()]","",Eliminar4)
            print(i)
            print(vddfi)
            for row in res:
                if vddfi!="ACTIVO":
                    self.tabla.setRowHidden(count, True)
                else:
                    self.id= row[0]
                    self.tabla.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                    self.tabla.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                    self.tabla.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
                    self.tabla.setItem(tablerow,3,QTableWidgetItem(str(row[3])))
                    self.tabla.setItem(tablerow,4,QTableWidgetItem(str(row[4])))
                    self.tabla.setItem(tablerow,5,QTableWidgetItem(str(row[5])))
                    self.tabla.setItem(tablerow,6,QTableWidgetItem(str(row[6])))
                    tablerow+=1
                count+=1

    def datosPrestamo(self):
        self.tabla=self.panel.tabla_Prestamos
        sql2="SELECT idPrestamo,idClientes,idUsuario,ISBM,F_d_sal,F_d_ent,F_d_enReal FROM Prestamo"
        res= consulta(sql2).fetchall()
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        colum=len(res[0])
        sql3="SELECT Activo FROM Prestamo"
        eliminar=consulta(sql3).fetchone()
        self.tableWidget = self.panel.tabla_Prestamos
        self.tableWidget.setRowCount(colum)
        tablerow=0
        count=0

        for i in eliminar:
            Verf=i
            Eliminar1=str(Verf)
            Eliminar2=re.sub(",","",Eliminar1)
            Eliminar3=re.sub("'","",Eliminar2)
            Eliminar4=re.sub("()","",Eliminar3)
            vddfi =re.sub("[()]","",Eliminar4)
            print(i)
            print(vddfi)
            for row in res:
                if vddfi!="ACTIVO":
                    self.tabla.setRowHidden(count, True)
                else:
                    self.id= row[0]
                    self.tabla.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                    self.tabla.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                    self.tabla.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
                    self.tabla.setItem(tablerow,3,QTableWidgetItem(str(row[3])))
                    self.tabla.setItem(tablerow,4,QTableWidgetItem(str(row[4])))
                    self.tabla.setItem(tablerow,5,QTableWidgetItem(str(row[5])))
                    self.tabla.setItem(tablerow,6,QTableWidgetItem(str(row[6])))
                    tablerow+=1
                count+=1
                
    #Elimina las filas 
    def eliminarFila(self,sql):
        filaSeleccionada = self.tabla.selectedItems()

        if filaSeleccionada:
            ret = QMessageBox.question(self, '¡ADVERTENCIA!' , "¿Seguro que desea eliminar esta fila?" , QMessageBox.Yes | QMessageBox.No)
            print(ret)
            if ret!=16384:
                fila = filaSeleccionada[0].text()
                fila2 = filaSeleccionada[0].row()
            else:
                if filaSeleccionada:
                        fila = filaSeleccionada[0].text()
                        fila2 = filaSeleccionada[0].row()
                        param2=(fila,)
                        consulta(sql,param2)
                        self.tabla.setRowHidden(fila2, True)
                        self.tabla.clearSelection()
        else:
            QMessageBox.critical(self, "Eliminar fila", "Seleccione una fila.   ", QMessageBox.Ok)

    def buscarAutores(self):
        name=self.panel.CdBuscar.text()
        sql="SELECT idAutores,Nombre,Nombre2,Apellido,Apellido2 FROM Autores WHERE Nombre LIKE ?"
        ultimo=len(name)
        letra=(name[0]+'%'+name[ultimo-1],)
        param=(letra,)
        datos=consulta(sql,letra).fetchall()
        print(datos)

        sql2="SELECT Activo FROM Autores WHERE Nombre LIKE ?"
        eliminar=consulta(sql2,letra).fetchone()
        Eliminar1=str(eliminar)
        Eliminar2=re.sub(",","",Eliminar1)
        Eliminar3=re.sub("'","",Eliminar2)
        Eliminar4=re.sub("()","",Eliminar3)
        vddfi =re.sub("[()]","",Eliminar4)
        
        for j in eliminar:
            Eliminar1=str(j)
            Eliminar2=re.sub(",","",Eliminar1)
            Eliminar3=re.sub("'","",Eliminar2)
            Eliminar4=re.sub("()","",Eliminar3)
            vddfi =re.sub("[()]","",Eliminar4)
            print(vddfi)
            if name!=('',):
                if datos!=[]:
                    if vddfi=='ACTIVO':
                        for row in datos:
                                    i=len(datos)
                                    self.panel.tabla_Autores.setRowCount(i)
                                    tablerow=0
                                    self.tabla.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                                    self.tabla.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                                    self.tabla.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
                                    self.tabla.setItem(tablerow,3,QTableWidgetItem(str(row[3])))
                                    self.tabla.setItem(tablerow,4,QTableWidgetItem(str(row[4])))
                                    tablerow+=1
                    else:QMessageBox.critical(self, "Error", "Autor no existente en el sistema ", QMessageBox.Ok)
                else:QMessageBox.critical(self, "Error", "Autor no existente en el sistema ", QMessageBox.Ok)
            else:QMessageBox.critical(self, "Error", "Escriba el nombre de un autor ", QMessageBox.Ok)

    def buscarLibros(self):
        name=(self.panel.LiBuscar.text(),)
        sql="SELECT ISBM,Titulo,F_Publicacion,num_pags,Editorial,Ejemplares,Genero FROM Libros WHERE Titulo=?"
        datos=consulta(sql,name).fetchall()

        sql2="SELECT Activo FROM Libros WHERE Titulo=?"
        eliminar=consulta(sql2,name).fetchone()
        Eliminar1=str(eliminar)
        Eliminar2=re.sub(",","",Eliminar1)
        Eliminar3=re.sub("'","",Eliminar2)
        Eliminar4=re.sub("()","",Eliminar3)
        vddfi =re.sub("[()]","",Eliminar4)
        
        print(vddfi)
        if name!=('',):
            if datos!=[]:
                if vddfi=='ACTIVO':
                    for row in datos:
                                i=len(datos)
                                self.panel.tabla_Libros.setRowCount(i)
                                tablerow=0
                                self.tabla.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                                self.tabla.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                                self.tabla.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
                                self.tabla.setItem(tablerow,3,QTableWidgetItem(str(row[3])))
                                self.tabla.setItem(tablerow,4,QTableWidgetItem(str(row[4])))
                                self.tabla.setItem(tablerow,5,QTableWidgetItem(str(row[6])))
                                self.tabla.setItem(tablerow,6,QTableWidgetItem(str(row[5])))
                                tablerow+=1
                else:QMessageBox.critical(self, "Error", "Libro no existente en el sistema ", QMessageBox.Ok)
            else:QMessageBox.critical(self, "Error", "Libro no existente en el sistema ", QMessageBox.Ok)
        else:QMessageBox.critical(self, "Error", "Escriba el Titulo de un libro ", QMessageBox.Ok)

    def buscarClientes(self):
        name=(self.panel.CCBuscar.text(),)
        sql="SELECT Cedula,Nombre,Nombre2,Apellido,Apellido2,Genero,FechaNa,EstatusCliente FROM Clientes WHERE Nombre=?"
        datos=consulta(sql,name).fetchall()

        sql2="SELECT Activo FROM Clientes WHERE Nombre=?"
        eliminar=consulta(sql2,name).fetchone()
        Eliminar1=str(eliminar)
        Eliminar2=re.sub(",","",Eliminar1)
        Eliminar3=re.sub("'","",Eliminar2)
        Eliminar4=re.sub("()","",Eliminar3)
        vddfi =re.sub("[()]","",Eliminar4)
        
        print(vddfi)
        if name!=('',):
            if datos!=[]:
                if vddfi=='ACTIVO':
                    for row in datos:
                                i=len(datos)
                                self.panel.tabla_Clientes.setRowCount(i)
                                tablerow=0
                                self.tabla.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                                self.tabla.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                                self.tabla.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
                                self.tabla.setItem(tablerow,3,QTableWidgetItem(str(row[3])))
                                self.tabla.setItem(tablerow,4,QTableWidgetItem(str(row[4])))
                                self.tabla.setItem(tablerow,5,QTableWidgetItem(str(row[5])))
                                self.tabla.setItem(tablerow,6,QTableWidgetItem(str(row[6])))
                                self.tabla.setItem(tablerow,7,QTableWidgetItem(str(row[7])))
                                tablerow+=1
                else:QMessageBox.critical(self, "Error", "Cliente no existente en el sistema ", QMessageBox.Ok)
            else:QMessageBox.critical(self, "Error", "Cliente no existente en el sistema ", QMessageBox.Ok)
        else:QMessageBox.critical(self, "Error", "Escriba el nombre de un Cliente ", QMessageBox.Ok)
        
    def buscarUsuarios(self):
        name=(self.panel.CUBuscar.text(),)
        sql="SELECT idUsuario,Nombre,Apellido,Username,Clave,email,Privilegios FROM Usuarios WHERE Nombre=?"
        datos=consulta(sql,name).fetchall()

        sql2="SELECT Activo FROM Usuarios WHERE Nombre=?"
        eliminar=consulta(sql2,name).fetchone()
        Eliminar1=str(eliminar)
        Eliminar2=re.sub(",","",Eliminar1)
        Eliminar3=re.sub("'","",Eliminar2)
        Eliminar4=re.sub("()","",Eliminar3)
        vddfi =re.sub("[()]","",Eliminar4)
        
        print(vddfi)
        if name!=('',):
            if datos!=[]:
                if vddfi=='ACTIVO':
                    for row in datos:
                                i=len(datos)
                                self.panel.tabla_Usuarios.setRowCount(i)
                                tablerow=0
                                self.tabla.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                                self.tabla.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                                self.tabla.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
                                self.tabla.setItem(tablerow,3,QTableWidgetItem(str(row[3])))
                                self.tabla.setItem(tablerow,4,QTableWidgetItem(str(row[4])))
                                self.tabla.setItem(tablerow,5,QTableWidgetItem(str(row[5])))
                                tablerow+=1
                else:QMessageBox.critical(self, "Error", "Usuario no existente en el sistema ", QMessageBox.Ok)
            else:QMessageBox.critical(self, "Error", "Usuario no existente en el sistema ", QMessageBox.Ok)
        else:QMessageBox.critical(self, "Error", "Escriba el nombre de un Usuario ", QMessageBox.Ok) 


    def verdatoAutores(self):
        filaSeleccionada = self.tabla.selectedItems()
        if filaSeleccionada:
            self.panel.NombreA.setText(filaSeleccionada[1].text())
            self.panel.Nombre2A.setText(filaSeleccionada[2].text())
            self.panel.ApellidoA.setText(filaSeleccionada[3].text())
            self.panel.Apellido2A.setText(filaSeleccionada[4].text())
        else:
            self.panel.NombreA.clear()
            self.panel.Nombre2A.clear()
            self.panel.ApellidoA.clear()
            self.panel.Apellido2A.clear()

    def verdatoLibros(self):
        filaSeleccionada = self.tabla.selectedItems()
        now=filaSeleccionada[2].text()
        fecha_dt = datetime.strptime(now,'%d/%m/%Y')
        if filaSeleccionada:
            self.panel.ISBML.setText(filaSeleccionada[0].text())
            self.panel.TituloL.setText(filaSeleccionada[1].text())
            self.panel.FechaPL.setDate(fecha_dt)
            self.panel.Nropags.setText(filaSeleccionada[3].text())
            self.panel.EditorialL.setText(filaSeleccionada[4].text())
            self.panel.EjemplaresL.setText(filaSeleccionada[6].text())
            self.panel.GeneroL.setText(filaSeleccionada[5].text())

    def verdatoClientes(self):
        filaSeleccionada = self.tabla.selectedItems()
        now=filaSeleccionada[7].text()
        fecha_dt = datetime.strptime(now,'%d/%m/%Y')
        if filaSeleccionada:
            Masculino=self.panel.ComboGC.itemText(2)
            Libre=self.panel.ComboEC.itemText(1)
            if Masculino == filaSeleccionada[6].text():
                self.panel.CedulaC.setText(filaSeleccionada[1].text())
                self.panel.NombreC.setText(filaSeleccionada[2].text())
                self.panel.Nombre2C.setText(filaSeleccionada[3].text())
                self.panel.ApellidoC.setText(filaSeleccionada[4].text())
                self.panel.Apellido2C.setText(filaSeleccionada[5].text())
                self.panel.FechaNC.setDate(fecha_dt)
                self.panel.ComboGC.setCurrentIndex(2)
                if Libre == filaSeleccionada[8].text():
                    self.panel.ComboEC.setCurrentIndex(1)
                else:
                    self.panel.ComboEC.setCurrentIndex(2)
            else:
                self.panel.CedulaC.setText(filaSeleccionada[1].text())
                self.panel.NombreC.setText(filaSeleccionada[2].text())
                self.panel.Nombre2C.setText(filaSeleccionada[3].text())
                self.panel.ApellidoC.setText(filaSeleccionada[4].text())
                self.panel.Apellido2C.setText(filaSeleccionada[5].text())
                self.panel.FechaNC.setDate(fecha_dt)
                self.panel.ComboGC.setCurrentIndex(1)
                if Libre == filaSeleccionada[8].text():
                    self.panel.ComboEC.setCurrentIndex(1)
                else:
                    self.panel.ComboEC.setCurrentIndex(2)
    
    def verdatoPrestamos(self):
        filaSeleccionada = self.tabla.selectedItems()
        now=filaSeleccionada[4].text()
        now1=filaSeleccionada[5].text()
        fecha_sal = datetime.strptime(now,'%d/%m/%Y')
        fecha_ent = datetime.strptime(now1,'%d/%m/%Y')
        if filaSeleccionada:
            self.panel.buscar_Cliente.setText(filaSeleccionada[1].text())
            self.panel.buscar_Libro.setText(filaSeleccionada[2].text())
            self.panel.dateEdit_2.setDate(fecha_sal)
            self.panel.dateEdit_3.setDate(fecha_ent)


    def verdatoUsuarios(self):
        filaSeleccionada = self.tabla.selectedItems()
        if filaSeleccionada:
            ma=self.panel.ComboGC_2.itemText(2)
            self.panel.NombreU.setText(filaSeleccionada[1].text())
            self.panel.ApellidoU.setText(filaSeleccionada[2].text())
            self.panel.UsernameU.setText(filaSeleccionada[3].text())
            self.panel.ClaveU.setText(filaSeleccionada[4].text())
            self.panel.EmailU.setText(filaSeleccionada[5].text())
            if ma==filaSeleccionada[6].text():
                self.panel.ComboGC_2.setCurrentIndex(2)
            else:
                self.panel.ComboGC_2.setCurrentIndex(1)
 
    def ModificarAutores(self):
        filaSeleccionada = self.tabla.selectedItems()
        sql="SELECT Nombre,Nombre2,Apellido,Apellido2 FROM Autores WHERE idAutores=?"
        fila=filaSeleccionada[0].text()
        dato=consulta(sql,fila).fetchone()
        Nombre=self.panel.NombreA.text()
        Nombre2=self.panel.Nombre2A.text()
        apellido=self.panel.ApellidoA.text()
        apellido2=self.panel.Apellido2A.text()
        Eliminar1=str(dato)
        Eliminar2=re.sub(",","",Eliminar1)
        Eliminar3=re.sub("'","",Eliminar2)
        Eliminar4=re.sub("()","",Eliminar3)
        vddfi =re.sub("[()]","",Eliminar4)
        print(vddfi)
        if filaSeleccionada:
            if Nombre.isalpha() and apellido.isalpha() and Nombre2.isalpha() and apellido2.isalpha():
                if vddfi!=Nombre+" "+Nombre2+" "+apellido+" "+apellido2:
                    ret = QMessageBox.question(self, '¡ADVERTENCIA!' , "¿Desea modificar esta fila?" , QMessageBox.Yes | QMessageBox.No)
                    if ret!=16384:
                        fila = filaSeleccionada[0].text()
                        fila2 = filaSeleccionada[0].row()
                    else:
                        sql="UPDATE Autores SET Nombre=?,Nombre2=?,Apellido=?,Apellido2=? WHERE idAutores=?"
                        param=(Nombre,Nombre2,apellido,apellido2,fila)
                        consulta(sql,param)
                        self.panel.NombreA.clear()
                        self.panel.Nombre2A.clear()
                        self.panel.ApellidoA.clear()
                        self.panel.Apellido2A.clear()
                        self.datosAutores()
                else:
                    QMessageBox.question(self, '¡Aviso!' , "No hay cambios encontrados" , QMessageBox.Ok)
            else:
                QMessageBox.question(self, '¡Aviso!' , "Los campos no pueden tener valores numericos, ni caracteres especiales" , QMessageBox.Ok)

    
    def ModificarLibros(self):
        filaSeleccionada = self.tabla.selectedItems()
        sql="SELECT ISBM,Titulo,F_Publicacion,num_pags,Editorial,Ejemplares,Genero FROM Libros WHERE ISBM=?"
        fila=(filaSeleccionada[0].text(),)
        dato=consulta(sql,fila).fetchone()
        print(dato)
        ISBMn=self.panel.ISBML.text()
        Titulo=self.panel.TituloL.text()
        now=self.panel.FechaPL.date()
        fecha=now.toPyDate()
        f1_str = fecha.strftime('%d/%m/%Y')
        Nropags=self.panel.Nropags.text()
        Editorial=self.panel.EditorialL.text()
        Ejemplares=self.panel.EjemplaresL.text()
        Genero=self.panel.GeneroL.text()
        Eliminar1=str(dato)
        Eliminar2=re.sub(",","",Eliminar1)
        Eliminar3=re.sub("'","",Eliminar2)
        Eliminar4=re.sub("()","",Eliminar3)
        vddfi =re.sub("[()]","",Eliminar4)
        print(vddfi)
        print(dato[0])

        if filaSeleccionada:
            if ISBMn==dato[0]:
                if Editorial.isalpha() and Genero.isalpha() and Ejemplares.isnumeric() and Nropags.isnumeric():
                    if vddfi!= ISBMn+" "+Titulo+" "+f1_str+" "+Nropags+" "+Editorial+" "+Ejemplares+" "+Genero:
                        ret = QMessageBox.question(self, '¡ADVERTENCIA!' , "¿Desea modificar esta fila?" , QMessageBox.Yes | QMessageBox.No)
                        if ret!=16384:
                            fila = filaSeleccionada[0].text()
                        else:
                            sql="UPDATE Libros SET Titulo=?,F_Publicacion=?,num_pags=?,Editorial=?,Ejemplares=?,Genero=? WHERE ISBM=?"
                            param=(Titulo,f1_str,Nropags,Editorial,Ejemplares,Genero,ISBMn)
                            consulta(sql,param)
                            self.datosLibros()
                    else:
                        QMessageBox.question(self, '¡Aviso!' , "No hay cambios encontrados" , QMessageBox.Ok)
                else:
                    QMessageBox.question(self, '¡Aviso!' , "Campos mal escritos" , QMessageBox.Ok)
            else:
                QMessageBox.question(self, '¡Aviso!' , "El ISBM no puede ser modificado" , QMessageBox.Ok)


    def ModificarUsuarios(self):
        filaSeleccionada = self.tabla.selectedItems()
        sql="SELECT Nombre,Apellido,Username,Clave,email,Privilegios FROM Usuarios WHERE idUsuario=?"
        fila=filaSeleccionada[0].text()
        dato=consulta(sql,fila).fetchone()
        Nombre=self.panel.NombreU.text()
        apellido=self.panel.ApellidoU.text()
        Username=self.panel.UsernameU.text()
        Clave=self.panel.ClaveU.text()
        email=self.panel.EmailU.text()
        Privilegios=self.panel.ComboGC_2.currentText()
        Eliminar1=str(dato)
        Eliminar2=re.sub(",","",Eliminar1)
        Eliminar3=re.sub("'","",Eliminar2)
        Eliminar4=re.sub("()","",Eliminar3)
        vddfi =re.sub("[()]","",Eliminar4)
        validacion=True
        
        if not re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',email.lower()):
            validacion = False
    

        if filaSeleccionada:
            if Nombre.isalpha() and apellido.isalpha() and self.validarClave(Clave):
                if validacion == True:
                    if vddfi!=Nombre+" "+apellido:
                        ret = QMessageBox.question(self, '¡ADVERTENCIA!' , "¿Desea modificar esta fila?" , QMessageBox.Yes | QMessageBox.No)
                        if ret!=16384:
                            fila = filaSeleccionada[0].text()
                        else:
                            sql="UPDATE Usuarios SET Nombre=?,Apellido=?,Username=?,Clave=?,email=?,Privilegios=? WHERE idUsuario=?"
                            param=(Nombre,apellido,Username,Clave,email,Privilegios,fila)
                            consulta(sql,param)
                            self.datosUsuarios()
                    else:
                        QMessageBox.question(self, '¡Aviso!' , "No hay cambios encontrados" , QMessageBox.Ok)
                else:
                     QMessageBox.question(self, '¡Aviso!' , "Correo no valido" , QMessageBox.Ok)
            else:
                QMessageBox.question(self, '¡Aviso!' , "Los campos no pueden tener valores numericos, ni caracteres especiales" , QMessageBox.Ok)
                

    def ModificarClientes(self):
        filaSeleccionada = self.tabla.selectedItems()
        if filaSeleccionada:
            sql="SELECT Cedula,Nombre,Nombre2,Apellido,Apellido2,Genero,FechaNa,EstatusCliente FROM Clientes WHERE idClientes=?"
            fila=filaSeleccionada[0].text()
            print(filaSeleccionada[0].text())
            dato=consulta(sql,fila).fetchone()
            Cedula=self.panel.CedulaC.text()
            Nombre=self.panel.NombreC.text()
            Nombre2=self.panel.Nombre2C.text()
            apellido=self.panel.ApellidoC.text()
            apellido2=self.panel.Apellido2C.text()
            Genero=self.panel.ComboGC.currentText()
            now=self.panel.FechaNC.date()
            fecha=now.toPyDate()
            f1_str = fecha.strftime('%d/%m/%Y')
            Estatus=self.panel.ComboEC.currentText()
            Eliminar1=str(dato)
            Eliminar2=re.sub(",","",Eliminar1)
            Eliminar3=re.sub("'","",Eliminar2)
            Eliminar4=re.sub("()","",Eliminar3)
            vddfi =re.sub("[()]","",Eliminar4)
            print(vddfi)
            print(Cedula+" "+Nombre+" "+Nombre2+" "+apellido+" "+apellido2+" "+Genero+" "+f1_str+" "+Estatus)
            if filaSeleccionada:
                if Nombre.isalpha() and apellido.isalpha() and Nombre2.isalpha() and apellido2.isalpha() and Cedula.isnumeric():
                    if vddfi!=Cedula+" "+Nombre+" "+Nombre2+" "+apellido+" "+apellido2+" "+Genero+" "+f1_str+" "+Estatus:
                        ret = QMessageBox.question(self, '¡ADVERTENCIA!' , "¿Desea modificar esta fila?" , QMessageBox.Yes | QMessageBox.No)
                        if ret!=16384:
                            fila = filaSeleccionada[0].text()
                        else:
                            sql="UPDATE Clientes SET Cedula=?,Nombre=?,Nombre2=?,Apellido=?,Apellido2=?,Genero=?,FechaNa=?,EstatusCliente=? WHERE idClientes=?"
                            param=(Cedula,Nombre,Nombre2,apellido,apellido2,Genero,f1_str,Estatus,fila,)
                            consulta(sql,param)
                            self.datosClientes()
                    else:
                        QMessageBox.question(self, '¡Aviso!' , "No hay cambios encontrados" , QMessageBox.Ok)
                else:
                    QMessageBox.question(self, '¡Aviso!' , "Los campos no pueden tener valores numericos, ni caracteres especiales" , QMessageBox.Ok)
        else:
            QMessageBox.question(self, '¡Aviso!' , "Seleccione un campo para modificar" , QMessageBox.Ok)


    def InsertarAutores(self):
        filaSeleccionada = self.tabla.selectedItems()
        if filaSeleccionada:
            QMessageBox.question(self, 'Error' , "No puede inserta un autor seleccionado" , QMessageBox.Ok)
            self.tabla.takeItem()
        else:
            sql="INSERT INTO Autores(Nombre,Nombre2,Apellido,Apellido2) VALUES (?,?,?,?)"
            Nombre=self.panel.NombreA.text()
            Nombre2=self.panel.Nombre2A.text()
            Apellido=self.panel.ApellidoA.text()
            Apellido2=self.panel.Apellido2A.text()
            param=(Nombre,Nombre2,Apellido,Apellido2)
            if Nombre!="" and Nombre2!="" and Apellido!="" and Apellido2!="":
                if Nombre.isalpha() and Nombre2.isalpha() and Apellido.isalpha() and Apellido2.isalpha():
                    consulta(sql,param)
                    self.panel.NombreA.clear()
                    self.panel.Nombre2A.clear()
                    self.panel.ApellidoA.clear()
                    self.panel.Apellido2A.clear()
                    QMessageBox.question(self, '¡EXITO!' , "Autores registrado exitosamente" , QMessageBox.Ok)
                else:
                    QMessageBox.question(self, '¡Aviso!' , "Los campos no pueden tener valores numericos, ni caracteres especiales" , QMessageBox.Ok)
            else:
                QMessageBox.question(self, '¡Aviso!' , "Inserte datos para continuar" , QMessageBox.Ok)

    def InsertarUsuarios(self):
        filaSeleccionada = self.tabla.selectedItems()
        if filaSeleccionada:
            QMessageBox.question(self, 'Error' , "No puede inserta un Usuario seleccionado" , QMessageBox.Ok)
            self.tabla.takeItem()
        else:
            sql="INSERT INTO Usuarios(Nombre,Apellido,username,Clave,email,Privilegios) VALUES (?,?,?,?,?,?)"
            Nombre=self.panel.NombreU.text()
            apellido=self.panel.ApellidoU.text()
            Username=self.panel.UsernameU.text()
            Clave=self.panel.ClaveU.text()
            email=self.panel.EmailU.text()
            Privilegios=self.panel.ComboGC_2.currentText()
            param=(Nombre,apellido,Username,Clave,email,Privilegios)
            validacion=True
        
            if not re.match('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$',email.lower()):
                validacion = False

            if Nombre!="" and apellido!="" and Username!="" and Clave!="" and email!="" and Privilegios!="Seleccione Privilegios:":
                if Nombre.isalpha() and apellido.isalpha() and validacion==True and self.validarClave(Clave):
                    consulta(sql,param)
                    self.panel.NombreU.clear()
                    self.panel.ApellidoU.clear()
                    self.panel.UsernameU.clear()
                    self.panel.ClaveU.clear()
                    self.panel.EmailU.clear()
                    self.panel.ComboGC_2.setCurrentIndex(0)
                    QMessageBox.question(self, '¡EXITO!' , "Usuario registrado exitosamente" , QMessageBox.Ok)
                else:
                    QMessageBox.question(self, '¡Aviso!' , "Los campos no pueden tener valores numericos, ni caracteres especiales" , QMessageBox.Ok)
            else:
                QMessageBox.question(self, '¡Aviso!' , "Inserte datos para continuar" , QMessageBox.Ok)


    def InsertarClientes(self):
        filaSeleccionada = self.tabla.selectedItems()
        if filaSeleccionada:
            QMessageBox.question(self, 'Error' , "No puede inserta un Cliente seleccionado" , QMessageBox.Ok)
            self.tabla.takeItem()
        else:
            sql="INSERT INTO Clientes(Cedula,Nombre,Nombre2,Apellido,Apellido2,Genero,fechaNa,EstatusCliente) VALUES (?,?,?,?,?,?,?,?)"
            Cedula=self.panel.CedulaC.text()
            Nombre=self.panel.NombreC.text()
            Nombre2=self.panel.Nombre2C.text()
            apellido=self.panel.ApellidoC.text()
            apellido2=self.panel.Apellido2C.text()
            Genero=self.panel.ComboGC.currentText()
            now=self.panel.FechaNC.date()
            fecha=now.toPyDate()
            f1_str = fecha.strftime('%d/%m/%Y')
            Estatus=self.panel.ComboEC.currentText()
            param=(Cedula,Nombre,Nombre2,apellido,apellido2,Genero,f1_str,Estatus)
            if Nombre!="" and Nombre2!="" and apellido!="" and apellido2!="" and Cedula!=""and Estatus!="Seleccione Estatus:" and Genero!="Seleccione un Género:":
                if Cedula.isnumeric() and Nombre.isalpha() and Nombre2.isalpha() and apellido.isalpha() and apellido2.isalpha():
                    consulta(sql,param)
                    self.panel.CedulaC.clear()
                    self.panel.NombreC.clear()
                    self.panel.Nombre2C.clear()
                    self.panel.ApellidoC.clear()
                    self.panel.Apellido2C.clear()
                    self.panel.ComboGC.setCurrentIndex(0)
                    self.panel.ComboEC.setCurrentIndex(0)
                    QMessageBox.question(self, '¡EXITO!' , "Autores registrado exitosamente" , QMessageBox.Ok)
                else:
                    QMessageBox.question(self, '¡Aviso!' , "Los campos no pueden tener valores numericos, ni caracteres especiales" , QMessageBox.Ok)
            else:
                QMessageBox.question(self, '¡Aviso!' , "Inserte datos para continuar" , QMessageBox.Ok)


    def InsertarLibros(self):
        filaSeleccionada = self.tabla.selectedItems()
        if filaSeleccionada:
            QMessageBox.question(self, 'Error' , "No puede inserta un Cliente seleccionado" , QMessageBox.Ok)
            self.tabla.takeItem()
        else:
            sql="INSERT INTO Libros(ISBM,Titulo,F_Publicacion,num_pags,Editorial,Ejemplares,Genero) VALUES (?,?,?,?,?,?,?)"
            ISBMn=self.panel.ISBML.text()
            Titulo=self.panel.TituloL.text()
            FechaP=self.panel.FechaPL.text()
            Nropags=self.panel.Nropags.text()
            Editorial=self.panel.EditorialL.text()
            Ejemplares=self.panel.EjemplaresL.text()
            Genero=self.panel.GeneroL.text()
            sql1="SELECT ISBM FROM Libros WHERE ISBM=?"
            param=(ISBMn,)
            verfi=consulta(sql1,param).fetchone()
            Eliminar1=str(verfi)
            Eliminar2=re.sub(",","",Eliminar1)
            Eliminar3=re.sub("'","",Eliminar2)
            Eliminar4=re.sub("()","",Eliminar3)
            vddfi =re.sub("[()]","",Eliminar4)
            print(vddfi)

            param=(ISBMn,Titulo,FechaP,Nropags,Editorial,Ejemplares,Genero)
            if ISBMn!="" and Titulo!="" and FechaP!="" and Nropags!="" and Editorial!=""and Ejemplares!="" and Genero!="":
                if Ejemplares.isnumeric() and Nropags.isnumeric() and Genero.isalpha():
                    if ISBMn!= vddfi:
                        consulta(sql,param)
                        self.panel.ISBML.clear()
                        self.panel.TituloL.clear()
                        self.panel.FechaPL.clear()
                        self.panel.Nropags.clear()
                        self.panel.EditorialL.clear()
                        self.panel.EjemplaresL.clear()
                        self.panel.GeneroL.clear()
                        QMessageBox.question(self, '¡EXITO!' , "Libro registrado exitosamente" , QMessageBox.Ok)
                    else:
                        QMessageBox.question(self, '¡Aviso!' , "ISBM no puede estar previamente registrado" , QMessageBox.Ok)
                else:
                    QMessageBox.question(self, '¡Aviso!' , "Los campos no pueden tener valores numericos, ni caracteres especiales" , QMessageBox.Ok)
            else:
                QMessageBox.question(self, '¡Aviso!' , "Inserte datos para continuar" , QMessageBox.Ok)




    def validarClave(self, clave):
        if len(clave) > 7 and len(clave) <= 25:
            minuscula = False
            mayuscula = False
            numero = False
            especial = False

            for char in clave:
                if (char.isdigit()):
                    numero = True
                if (char.islower()):
                    minuscula = True
                if (char.isupper()):
                    mayuscula = True
                if (not char.isalnum()):
                    especial = True
            if minuscula and mayuscula and numero and especial:
                return True
            else:
                QMessageBox.critical(self, "Aviso", "La contraseña debe tener letras mayusculas, minusculas, numeros y caracteres especiales", QMessageBox.Ok)
                return False
        else:
            QMessageBox.critical(self, "Aviso", "La contraseña debe tener entre 8 y 25 caracteres", QMessageBox.Ok)
            return False


    def autoresIr(self):
        self.panel.stackedWidget.setCurrentIndex(4)
        self.datosAutores()


    def prestamosIr(self):
        self.panel.stackedWidget.setCurrentIndex(5)
        self.datosPrestamo()

    def estadisticasIr(self):
        self.panel.stackedWidget.setCurrentIndex(6)
        self.cargarEstadisticas()
        

    def cargarEstadisticas(self):
        # Estos datos deben ser cambiados por los de la bdd

        # Numero de usuarios registrados
        self.panel.userNumLabel.setText("22")

        # Numero de clientes registrados
        self.panel.clientesNumLabel.setText("12")

        # Numero de libros en la biblioteca
        self.panel.librosNumLabel.setText("1100")

        # Numero de prestamos totales
        self.panel.prestNumLabel.setText("144")

        # Numero de libros prestados actualmente
        self.panel.librosPrestLabel.setText("10")


        self.creaDona(30, 70)
        self.creaBarras("Libro1", 120, "Libro2", 80, "Libro3", 50)

    # Crea un png del grafico de barras
    def creaBarras(self, libro1, numero1, libro2, numero2, libro3, numero3):

        # Datos del grafico
        numLibros = [0, 0, 0]
        titulos = ["", "", ""]

        titulos[0] = libro1
        titulos[1] = libro2
        titulos[2] = libro3

        numLibros[0] = numero1
        numLibros[1] = numero2
        numLibros[2] = numero3

        # Cantidad de posiciones en el gráfico
        positions = range(len(numLibros))

        # Limpia figuras previas
        plt.clf()

        # Estilo del grafico
        plt.style.use("ggplot")

        # Grafico de barras
        plt.bar(positions, numLibros)

        # Remplaza los labels
        plt.xticks(positions, titulos)

        # Guarda el grafico como un png
        plt.savefig("reportes/barras.png", dpi=100)


    # Crea un png del grafico de Dona
    def creaDona(self, aTiempo, tarde):

        # Datos del grafico
        labels = ["A tiempo", "Tarde"]
        datos = [0, 0]
        datos[0] = aTiempo
        datos[1] = tarde

        # Limpia figuras previas
        plt.clf()

        # Estilo del grafico
        plt.style.use("ggplot")

        # Grafico de pie (datos, titulos, porcentajes, donde comienza el primer angulo)
        plt.pie(x=datos, labels=labels, autopct="%.2f%%", startangle=90)

        # Mantiene una relacion 1:1 con respecto a la altura y la anchura del grafico
        plt.axis("equal")

        # Pone un circulo blanco para hacer el grafico una dona
        circle = plt.Circle(xy=(0,0), radius=.70, facecolor="white")
        plt.gca().add_artist(circle)

        # Guarda el grafico como un png
        plt.savefig("reportes/dona.png")


    def reportesIr(self):
        self.panel.stackedWidget.setCurrentIndex(7)

    def reporteEst(self):
        # Cambiar datos por los de la bdd
        consul="SELECT COUNT(*) FROM Prestamo WHERE ISBM=?"
        param=("213de",)
        print(consulta(consul,param))
        self.creaDona(30, 70)

        self.creaBarras("Libro1", 120, "Libro2", 80, "Libro3", 50)

        # Abre File Dialog
        rutadestino = QFileDialog.getExistingDirectory(self, caption="Selecciona Ubicación")

        # si se cancela la accion no se procede con el prestamo
        if not rutadestino:
            return
        else:
            # Cambiar datos por los de la bdd
            self.generarReporteEst(rutadestino, "12", "124", "1201", "121", "12")

    def reportePres(self):
        idPrest = self.panel.idPresReporte.text()
        if idPrest.isdigit():
            # aqui se toman los datos de la bdd

            # Verifica que el correo ingresado este en la bdd
            sql="SELECT Activo FROM Prestamo WHERE idPrestamo=?"
            param=(idPrest,) 
            dato=consulta(sql,param).fetchone()
            Eliminar1=str(dato)
            Eliminar2=re.sub(",","",Eliminar1)
            Eliminar3=re.sub("'","",Eliminar2)
            Eliminar4=re.sub("()","",Eliminar3)
            presid =re.sub("[()]","",Eliminar4)

            if presid != "None":
                # Abre File Dialog
                rutadestino = QFileDialog.getExistingDirectory(self, caption="Selecciona Ubicación")

                if not rutadestino:
                    return
                else:
                    # select datos del prestamo aqui
                    # Cambiar datos por los de la bdd
                    self.generarReportePres(rutadestino, idPrest, "cedula", "nombre", "ISBN del libro", "titulo del libro", "autor del libro", "fecha del prestamo", "fecha de devolucion")
            else:
                QMessageBox.critical(self, "Aviso", "ID de préstamo inválido")
        else:
            # Si el id ingresado no es un numero valido se envia este mensaje
            QMessageBox.question(self, 'Error' , "El número ingresado no es válido" , QMessageBox.Ok)

    # Función para generar reportes de estadisticas
    def generarReporteEst(self, ruta, users, clientes, libros, prestamos, librosPrestados):

        # Obtiene la ubicacion absoluta de las imagenes
        pathBarras = os.path.abspath(r"reportes\barras.png")
        pathDona = os.path.abspath(r"reportes\dona.png")

        dt = datetime.now()
        fecha = "{}-{}-{}".format(dt.day, dt.month, dt.year)

        # Diccionario para cambiar las {{variables}} por sus valores correspondientes
        context = {
            "fecha": fecha,
            "pathBarras": pathBarras,
            "pathDona": pathDona,
            "users": users,
            "clientes": clientes,
            "libros": libros,
            "prestamos": prestamos,
            "librosPrestados": librosPrestados
        }

        # Carga la plantilla HTML
        templateLoader = jinja2.FileSystemLoader("./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template("reportes/estadisticas.html")

        # Reemplaza las {{variables}} usando el diccionario
        outpuText = template.render(context)

        #Hace que pdfkit detecte wkhtmltopdf
        pathPDF = os.path.abspath(r"wkhtmltopdf\bin\wkhtmltopdf.exe") 
        config = pdfkit.configuration(wkhtmltopdf=pathPDF)

        # Indica el nombre que tendrá el archivo pdf
        outputPDF = ruta + "/Estadísticas" + fecha + ".pdf"

        options = {'enable-local-file-access': None}

        # Crea el pdf a partir del archivo html
        pdfkit.from_string(outpuText, outputPDF, configuration=config, options=options)

    # Función para generar reportes de prestamos
    def generarReportePres(self, ruta, numpres, cedula, nombre, idlibro, titulo, autor, fechapres, fechadev):

        # Diccionario para cambiar las {{variables}} por sus valores correspondientes
        context = {
            "numpres": numpres, 
            "cedula": cedula, 
            "nombre": nombre, 
            "idlibro": idlibro, 
            "titulo": titulo, 
            "autor": autor, 
            "fechapres": fechapres, 
            "fechadev": fechadev
        }

        # Carga la plantilla HTML
        templateLoader = jinja2.FileSystemLoader("./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template("reportes/prestamo.html")

        outpuText = template.render(context)

        #Hace que pdfkit detecte wkhtmltopdf
        pathPDF = os.path.abspath(r"wkhtmltopdf\bin\wkhtmltopdf.exe") 
        config = pdfkit.configuration(wkhtmltopdf=pathPDF)

        # Indica el nombre que tendrá el archivo pdf
        outputPDF = ruta + "/Préstamo" + numpres + ".pdf"

        # Crea el pdf a partir del archivo html
        pdfkit.from_string(outpuText, outputPDF, configuration=config)

    def respaldarBDD(self):
        # Abre File Dialog
        rutadestino = QFileDialog.getExistingDirectory(self, caption="Selecciona Ubicación")
        
        if not rutadestino:
            return
        else:
            # Copia la bdd en la ruta destino
            shutil.copy2("Bibliotkmdb.db", rutadestino)

    def restaurarBDD(self):
        # Abre File Dialog
        rutadestino = QFileDialog.getOpenFileName(self, caption="Selecciona el archivo")

        if rutadestino[0] == "":
            return
        else:
            # Inserte validaciones aqui xdxdxd

            # Verifica que el nombre del archivo sea el mismo
            ruta = os.path.normpath(rutadestino[0])
            nombreArchivo = ruta.split(os.sep)[-1]

            print(nombreArchivo)
            if nombreArchivo == "Bibliotkmdb.db":
                # Copia la bdd en la ruta destino
                QMessageBox.information(self, "Aviso", "El programa se cerrará para efectuar los cambios", QMessageBox.Ok)
                shutil.copy2(rutadestino, "Bibliotkmdb.db")
                pass
            else:
                QMessageBox.critical(self, "Aviso", "Archivo inválido")

    def usuariosIr(self):
        self.panel.stackedWidget.setCurrentIndex(9)
        self.datosUsuarios()

    def acercaDe(self):
        msgAbout = QMessageBox()
        msgAbout.setWindowTitle("Acerca de")
        msgAbout.setText("Bibliotk")
        msgAbout.setInformativeText("Versión: 1.0.0 \n Copyright© Universidad Rafael Belloso Chacín ")
        msgAbout.setIcon(QMessageBox.Information)
        msgAbout.setStandardButtons(QMessageBox.Ok)
        msgAbout.exec()

    def abrirManual(self):
        # Abre el manual de usuario en una pestaña del navegador predeterminado
        path = "Manual de Usuario.pdf"
        rutaCompleta = os.path.abspath(path)
        if os.path.exists(rutaCompleta):
            webbrowser.open_new_tab(path)
        else:
            QMessageBox.critical(self, "No se puede abrir el archivo", "Es posible que el archivo haya sido eliminado o se haya movido de lugar", QMessageBox.Ok)

# if __name__ == "__main__":
#     # Crea la app de Pyqt5
#     app = QApplication([])

#     # Crea la instancia de nuestra ventana
#     window = PanelControl()
#     window.usuario = "1"
#     window.privilegios()

#     # Muestra la ventana
#     window.show()

#     # Ejecuta la app
#     app.exec_()