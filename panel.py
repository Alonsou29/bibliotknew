import sys
import os
from PyQt5 import uic
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
<<<<<<< HEAD
from datetime import *
=======
import datetime
from email.message import EmailMessage
import ssl
import smtplib
import random
>>>>>>> b94cf923af152335ca4e8edcb018cee0d7e582d1

class PanelControl(QMainWindow):

    # Constructor del frame
    def __init__(self):
        super().__init__()
        # Carga Panel de cotrol
        self.panel = uic.loadUi("frames\panel.ui",self)

        # Establece titulo de la ventana
        self.panel.setWindowTitle("Bibliotk")

        # Establece el tamaño de la ventana y hace que no puedas cambiar su tamaño
        self.panel.setFixedSize(800, 600) # (Ancho, Alto)

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

        # Variable que usaremos para codigos de verificacion en correos
        self.verifCode = 0

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
        EliminarUsql="UPDATE Usuarios SET Activo = 'INACTIVO' WHERE idUsuarios=?"
        self.panel.EliminarU.clicked.connect(lambda:self.eliminarFila(EliminarUsql))
        self.panel.RefrescarU.clicked.connect(lambda:self.datosUsuarios())

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

            #Insertar datos
        self.panel.NuevoA.clicked.connect(lambda:self.Insertar())

            # Generar Reportes
        self.panel.Generar_Reportes_E.clicked.connect(lambda:self.reporteEst()) # Estadisticas
        self.panel.Generar_Reportes_P.clicked.connect(lambda:self.reportePres()) # Prestamos

    # Funciones del menubar
    def inicioIr(self):
        # Camabia la pantalla a la seleccionada
        self.panel.stackedWidget.setCurrentIndex(0)

    def perfilIr(self):
        self.panel.stackedWidget.setCurrentIndex(1)
        # Este dato hay que cambiarlo de acuerdo a la bdd
        verificado = False
        if not verificado:
            self.verificarCorreo()

    def verificarCorreo(self):

        self.verifCode = random.randint(100000, 999999)

        # tomar email con bdd
        email = "mariana.duque.uni@gmail.com"

        # Enviamos codigo de verificacion por correo
        # El asunto y el cuerpo del correo
        asuntoCorreo = "Verificación de Email"
        cuerpoCorreo = """Estimado usuario, gracias por usar nuestros servicios. 
        
        Para verificar su correo ingrese en su perfil el siguiente código: 
        
        Código de verificación: """ + str(self.verifCode) + """

        Bibliotk Software"""
        # print(str(self.verifCode))
        self.enviarCorreo(email, asuntoCorreo, cuerpoCorreo)
        
        numeroCorrecto = False

        while not numeroCorrecto:
            numero, estado = QInputDialog().getText(self, "Verificar Correo", "Para verificar su correo electrónico le hemos enviado\nun código de verificación, ingrese el código aquí: ")
            if estado:
                if numero.isdigit():
                    if numero == str(self.verifCode):
                        # En bdd cambiar verificado a true
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
        name=(self.panel.CdBuscar.text(),)
        sql="SELECT idAutores,Nombre,Apellido FROM Autores WHERE Nombre=?"
        datos=consulta(sql,name).fetchall()

        sql2="SELECT Activo FROM Autores WHERE Nombre=?"
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
                                self.panel.tabla_Autores.setRowCount(i)
                                tablerow=0
                                self.tabla.setItem(tablerow,0,QTableWidgetItem(str(row[0])))
                                self.tabla.setItem(tablerow,1,QTableWidgetItem(str(row[1])))
                                self.tabla.setItem(tablerow,2,QTableWidgetItem(str(row[2])))
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

    def verdatoLibros(self):
        filaSeleccionada = self.tabla.selectedItems()
        if filaSeleccionada:
            self.panel.ISBML.setText(filaSeleccionada[0].text())
            self.panel.TituloL.setText(filaSeleccionada[1].text())
            self.panel.FechaPL.setText(filaSeleccionada[2].text())
            self.panel.Nropags.setText(filaSeleccionada[3].text())
            self.panel.EditorialL.setText(filaSeleccionada[4].text())
            self.panel.EjemplaresL.setText(filaSeleccionada[6].text())
            self.panel.GeneroL.setText(filaSeleccionada[5].text())

    def verdatoClientes(self):
        filaSeleccionada = self.tabla.selectedItems()
        now=filaSeleccionada[7].text()
        fecha_dt = datetime.strptime(now, '%d/%m/%Y')
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
        FechaP=self.panel.FechaPL.text()
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
                    if vddfi!= ISBMn+" "+Titulo+" "+FechaP+" "+Nropags+" "+Editorial+" "+Ejemplares+" "+Genero:
                        ret = QMessageBox.question(self, '¡ADVERTENCIA!' , "¿Desea modificar esta fila?" , QMessageBox.Yes | QMessageBox.No)
                        if ret!=16384:
                            fila = filaSeleccionada[0].text()
                        else:
                            sql="UPDATE Libros SET Titulo=?,F_Publicacion=?,num_pags=?,Editorial=?,Ejemplares=?,Genero=? WHERE ISBM=?"
                            param=(Titulo,FechaP,Nropags,Editorial,Ejemplares,Genero,ISBMn)
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
            if Nombre.isalpha() and apellido.isalpha():
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


    def Insertar(self):
        
        sql="INSERT INTO Autores(Nombre,Nombre2,Apellido,Apellido2) VALUES (?,?,?,?)"
        Nombre=self.panel.NombreA.text()
        Nombre2=self.panel.Nombre2A.text()
        Apellido=self.panel.ApellidoA.text()
        Apellido2=self.panel.Apellido2A.text()
        param=(Nombre,Nombre2,Apellido,Apellido2)
        if Nombre!="" and Nombre2!="" and Apellido!="" and Apellido2!="":
            consulta(sql,param)






    def autoresIr(self):
        self.panel.stackedWidget.setCurrentIndex(4)
        self.datosAutores()


    def prestamosIr(self):
        self.panel.stackedWidget.setCurrentIndex(5)

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
            # Abre File Dialog
            rutadestino = QFileDialog.getExistingDirectory(self, caption="Selecciona Ubicación")

            if not rutadestino:
                return
            else:
                # Cambiar datos por los de la bdd
                self.generarReportePres(rutadestino, idPrest, "cedula", "nombre", "ISBN del libro", "titulo del libro", "autor del libro", "fecha del prestamo", "fecha de devolucion")
        else:
            # Si el id ingresado no es un numero valido se envia este mensaje
            QMessageBox.question(self, 'Error' , "El número ingresado no es válido" , QMessageBox.Ok)

    # Función para generar reportes de estadisticas
    def generarReporteEst(self, ruta, users, clientes, libros, prestamos, librosPrestados):

        # Obtiene la ubicacion absoluta de las imagenes
        pathBarras = os.path.abspath(r"reportes\barras.png")
        pathDona = os.path.abspath(r"reportes\dona.png")

        dt = datetime.datetime.now()
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
        
        # Inserte validaciones aqui xdxdxd
        if rutadestino[0] == "":
            return
        else:
            # Hay que enviar un mensaje indicando que el programa se cerrara despues de seleccionar la bdd
            # Copia la bdd en la ruta destino
            shutil.copy2(rutadestino, "Bibliotkmdb.db")

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
        path = "manual_usuario.pdf"
        webbrowser.open_new_tab(path)

if __name__ == "__main__":
    # Crea la app de Pyqt5
    app = QApplication([])

    # Crea la instancia de nuestra ventana
    window = PanelControl()

    # Muestra la ventana
    window.show()

    # Ejecuta la app
    app.exec_()