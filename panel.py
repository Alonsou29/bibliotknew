import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow,QApplication,QMessageBox,QStackedWidget, QFileDialog,QTableWidgetItem,QAbstractItemView)
from PyQt5.QtSql import *
from conexion import consulta
from PyQt5.QtSql import *
import re
import shutil
import webbrowser
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#import matplotlib.pyplot as plt


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

        #FUNCIONES DE LOS BOTONES

            #Funcion Buscar
        self.panel.BuscarA.clicked.connect(lambda:self.buscarAutores())
        self.panel.BuscarL.clicked.connect(lambda:self.buscarLibros())
        self.panel.BuscarC.clicked.connect(lambda:self.buscarClientes())



            #Eliminar Autores
        EliminarAsql="UPDATE Autores SET Activo = 'INACTIVO' WHERE idAutores=?"
        self.panel.EliminarA.clicked.connect(lambda:self.eliminarFila(EliminarAsql))
        self.panel.RefrescarA.clicked.connect(lambda:self.datosAutores())

            #Eliminar Libros
        EliminarLsql="UPDATE Libros SET Activo = 'INACTIVO' WHERE ISBM=?"
        self.panel.EliminarL.clicked.connect(lambda:self.eliminarFila(EliminarLsql))
        self.panel.RefrescarL.clicked.connect(lambda:self.datosLibros())

            #Eliminar Clientes
        EliminarCsql="UPDATE Clientes SET Activo = 'INACTIVO' WHERE idClientes=?"
        self.panel.EliminarC.clicked.connect(lambda:self.eliminarFila(EliminarCsql))
        self.panel.RefrescarC.clicked.connect(lambda:self.datosClientes())

            #Eliminar Usuarios
        EliminarUsql="UPDATE Usuarios SET Activo = 'INACTIVO' WHERE idUsuario=?"
        self.panel.EliminarU.clicked.connect(lambda:self.eliminarFila(EliminarUsql))

            #Modifica Autores
        self.panel.tabla_Autores.clicked.connect(lambda:self.verdatoAutores())
        self.panel.ModificarA.clicked.connect(lambda:self.ModificarAutores())

            #Modificar Libros
        self.panel.tabla_Libros.clicked.connect(lambda:self.verdatoLibros())
        self.panel.ModificarL.clicked.connect(lambda:self.ModificarLibros())

            #Modificar Clientes
        self.panel.tabla_Clientes.clicked.connect(lambda:self.verdatoClientes())

        

            #Modificar Usuarios
        self.panel.tabla_Usuarios.clicked.connect(lambda:self.verdatoUsuarios())
        self.panel.ModificarU.clicked.connect(lambda:self.ModificarUsuarios())
            # Generar Reportes
        # self.panel.Generar_Reportes_E.clicked.connect(self.generarReporteEst()) # Estadisticas
        # self.panel.Generar_Reportes_P.clicked.connect(self.generarReportePres()) # Prestamos

    # Funciones del menubar
    def inicioIr(self):
        # Camabia la pantalla a la seleccionada
        self.panel.stackedWidget.setCurrentIndex(0)

    def perfilIr(self):
        self.panel.stackedWidget.setCurrentIndex(1)

    def clientesIr(self):
        self.panel.stackedWidget.setCurrentIndex(2)
        self.datosClientes()
        
    def librosIr(self):
        self.panel.stackedWidget.setCurrentIndex(3)
        self.datosLibros()
   

   #Muestra los datos de cliente
    def datosClientes(self):
        self.tabla=self.panel.tabla_Clientes
        sql="SELECT Cedula,Nombre,Apellido,Genero,FechaNa,EstatusCliente FROM Clientes"
        res= consulta(sql).fetchall()
        colum=len(res)
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget = self.panel.tabla_Clientes
        self.tableWidget.setRowCount(colum)
        sql3="SELECT Activo FROM Clientes"
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
                    tablerow+=1
            count+=1

    #Muestra los datos de usuarios
    def datosUsuarios(self):
        self.tabla=self.panel.tabla_Usuarios
        sql2="SELECT idUsuario,Nombre,Apellido,Username,Clave,email,Privilegios FROM Usuarios"
        res= consulta(sql2).fetchone()
        colum=len(res[0])
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget = self.panel.tabla_Usuarios
        self.tableWidget.setRowCount(colum)
        sql3="SELECT Activo FROM Usuarios"
        eliminar=consulta(sql3).fetchall()
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
        sql2="SELECT idAutores,Nombre,Apellido FROM Autores"
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
        sql="SELECT Cedula,Nombre,Apellido,Genero,FechaNa,EstatusCliente FROM Clientes WHERE Nombre=?"
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
                                tablerow+=1
                else:QMessageBox.critical(self, "Error", "Cliente no existente en el sistema ", QMessageBox.Ok)
            else:QMessageBox.critical(self, "Error", "Cliente no existente en el sistema ", QMessageBox.Ok)
        else:QMessageBox.critical(self, "Error", "Escriba el nombre de un Cliente ", QMessageBox.Ok)
        
        

    def verdatoAutores(self):
        filaSeleccionada = self.tabla.selectedItems()
        if filaSeleccionada:
            self.panel.NombreA.setText(filaSeleccionada[1].text())
            self.panel.ApellidoA.setText(filaSeleccionada[2].text())

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
        if filaSeleccionada:
            Masculino=self.panel.CoboGC.itemText(2)
            if Masculino == filaSeleccionada[3].text():
                self.panel.CedulaC.setText(filaSeleccionada[0].text())
                self.panel.NombreC.setText(filaSeleccionada[1].text())
                self.panel.ApellidoC.setText(filaSeleccionada[2].text())
                self.panel.FechaC.setText(filaSeleccionada[4].text())
                self.panel.CoboGC.setCurrentIndex(2)
            else:
                self.panel.CedulaC.setText(filaSeleccionada[0].text())
                self.panel.NombreC.setText(filaSeleccionada[1].text())
                self.panel.ApellidoC.setText(filaSeleccionada[2].text())
                self.panel.FechaC.setText(filaSeleccionada[4].text())
                self.panel.CoboGC.setCurrentIndex(1)
    
    def verdatoUsuarios(self):
        filaSeleccionada = self.tabla.selectedItems()
        if filaSeleccionada:
            self.panel.NombreU.setText(filaSeleccionada[1].text())
            self.panel.ApellidoU.setText(filaSeleccionada[2].text())
            self.panel.UsernameU.setText(filaSeleccionada[3].text())
            self.panel.ClaveU.setText(filaSeleccionada[4].text())
            self.panel.EmailU.setText(filaSeleccionada[5].text())
            self.panel.PrivilegiosU.setText(filaSeleccionada[6].text())
 
    def ModificarAutores(self):
        filaSeleccionada = self.tabla.selectedItems()
        sql="SELECT Nombre,Apellido FROM Autores WHERE idAutores=?"
        fila=filaSeleccionada[0].text()
        dato=consulta(sql,fila).fetchone()
        Nombre=self.panel.NombreA.text()
        apellido=self.panel.ApellidoA.text()
        Eliminar1=str(dato)
        Eliminar2=re.sub(",","",Eliminar1)
        Eliminar3=re.sub("'","",Eliminar2)
        Eliminar4=re.sub("()","",Eliminar3)
        vddfi =re.sub("[()]","",Eliminar4)
        print(vddfi)
        if filaSeleccionada:
            if Nombre.isalpha() and apellido.isalpha():
                if vddfi!=Nombre+" "+apellido:
                    ret = QMessageBox.question(self, '¡ADVERTENCIA!' , "¿Desea modificar esta fila?" , QMessageBox.Yes | QMessageBox.No)
                    if ret!=16384:
                        fila = filaSeleccionada[0].text()
                        fila2 = filaSeleccionada[0].row()
                    else:
                        sql="UPDATE Autores SET Nombre=?,Apellido=? WHERE idAutores=?"
                        param=(Nombre,apellido,fila,)
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
        Privi=self.panel.PrivilegiosU.text()
        Eliminar1=str(dato)
        Eliminar2=re.sub(",","",Eliminar1)
        Eliminar3=re.sub("'","",Eliminar2)
        Eliminar4=re.sub("()","",Eliminar3)
        vddfi =re.sub("[()]","",Eliminar4)
        
        if filaSeleccionada:
            if Nombre.isalpha() and apellido.isalpha():
                if vddfi!=Nombre+" "+apellido:
                    ret = QMessageBox.question(self, '¡ADVERTENCIA!' , "¿Desea modificar esta fila?" , QMessageBox.Yes | QMessageBox.No)
                    if ret!=16384:
                        fila = filaSeleccionada[0].text()
                    else:
                        sql="UPDATE Usuarios SET Nombre=?,Apellido=?,Username=?,Clave=?,email=?,Privilegios=? WHERE idUsuario=?"
                        param=(Nombre,apellido,Username,Clave,email,Privi,fila)
                        consulta(sql,param)
                        self.datosAutores()
                else:
                    QMessageBox.question(self, '¡Aviso!' , "No hay cambios encontrados" , QMessageBox.Ok)
            else:
                QMessageBox.question(self, '¡Aviso!' , "Los campos no pueden tener valores numericos, ni caracteres especiales" , QMessageBox.Ok)

               
    def autoresIr(self):
        self.panel.stackedWidget.setCurrentIndex(4)
        self.datosAutores()


    def prestamosIr(self):
        self.panel.stackedWidget.setCurrentIndex(5)

    def estadisticasIr(self):
        self.panel.stackedWidget.setCurrentIndex(6)

    def reportesIr(self):
        self.panel.stackedWidget.setCurrentIndex(7)

    def respaldarBDD(self):
        # Abre File Dialog
        rutadestino = QFileDialog.getExistingDirectory(self, caption="Selecciona Ubicación")
        
        # Copia la bdd en la ruta destino
        shutil.copy2("Bibliotkmdb.db", rutadestino)

    def restaurarBDD(self):
        # Abre File Dialog
        rutadestino = QFileDialog.getOpenFileName(self, caption="Selecciona el archivo")
        
        # Inserte validaciones aqui xdxdxd
        
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