import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QMainWindow,QApplication,QMessageBox,QStackedWidget, QFileDialog,QTableWidgetItem,QAbstractItemView)
from PyQt5.QtSql import *
from conexion import consulta
from BDDActions import Metodosbdd
from PyQt5.QtSql import *
import re
import shutil
import webbrowser


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
        self.panel.actionRegistrosP.triggered.connect(self.prestamosIr) # Prestamos
        self.panel.actionMostrarE.triggered.connect(self.estadisticasIr) # Estadisticas
        self.panel.actionMostrarR.triggered.connect(self.reportesIr) # Reportes
        self.panel.actionRespaldar.triggered.connect(self.respaldarBDD) # Mantenimiento: Respaldar BDD
        self.panel.actionRestaurar.triggered.connect(self.restaurarBDD) # Mantenimiento: Restaurar BDD
        self.panel.actionRegistrosU.triggered.connect(self.usuariosIr) # Usuarios
        self.panel.actionAcerca_de.triggered.connect(self.acercaDe) # Ayuda: Acerca de
        self.panel.actionManual_de_Usuario.triggered.connect(self.abrirManual) # Ayuda: Manual de usuario

        #FUNCIONES DE LOS BOTONES

            #Eliminar Autores
        EliminarAsql="UPDATE Autores SET Activo = 'INACTIVO' WHERE idAutores=?"
        self.panel.EliminarA.clicked.connect(lambda:self.eliminarFila(EliminarAsql))

            #Eliminar Libros
        EliminarLsql="UPDATE Libros SET Activo = 'INACTIVO' WHERE ISBM=?"
        self.panel.EliminarL.clicked.connect(lambda:self.eliminarFila(EliminarLsql))

            #Eliminar Usuarios
        EliminarUsql="UPDATE Clientes SET Activo = 'INACTIVO' WHERE idClientes=?"
        self.panel.EliminarC.clicked.connect(lambda:self.eliminarFila(EliminarUsql))

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
        sql="SELECT idClientes,Cedula,Nombre,Apellido,Genero,FechaNa,EstatusCliente FROM Clientes"
        res= consulta(sql).fetchall()
        colum=len(res[0])
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget = self.panel.tabla_Clientes
        self.tableWidget.setRowCount(colum)
        sql3="SELECT Activo FROM Clientes"
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


    #Muestra los datos de usuarios
    ''' def datosUsuarios(self):
        self.tabla=self.panel.tabla_Clientes
        sql2="SELECT idEmpleados,Nombre,Apellido,Username,Clave,email,Privilegios FROM Usuarios"
        res= consulta(sql2).fetchall()
        colum=len(res[0])
        self.tableWidget.setRowCount(colum)
        tablerow=0
        sql3="SELECT Activo FROM Usuarios"
        eliminar=consulta(sql3).fetchall()
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
            count+=1'''

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
        eliminar=consulta(sql3).fetchall()
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

    #def Modificar(self,sql):
    

               
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