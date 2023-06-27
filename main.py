import typing
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QMessageBox
from PyQt5 import QtCore, uic
from panel import PanelControl
from conexion import consulta
import sqlite3
import re



# Clase de la ventana principal
class MainWindow(QMainWindow):

    # Constructor
    def __init__(self):
        super().__init__()
        
        # Establece el titulo de la ventana
        self.setWindowTitle("Bibliotk")

        # Establece el tamaño de la ventana y hace que no puedas cambiar su tamaño
        self.setFixedSize(800, 600) # (Ancho, Alto)

        # Crea instancia de QStackedWidget
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Crea y agrega frames al stacked widget
        self.addFrame("frames\main.ui")
        self.addFrame("frames\login.ui")

        # Te lleva al login al presionar el boton de inicio
        self.stacked_widget.widget(0).Inicio.clicked.connect(self.loginIr)

        self.stacked_widget.widget(1).Seguir.clicked.connect(self.panelIr)
    

    # Funcion para agregar los frames al stacked widget
    def addFrame(self, ui_file):
        # Carga el archivo ui para el frame
        frame = uic.loadUi(ui_file)

        # Agrega el frame al stacked widget
        self.stacked_widget.addWidget(frame)


    # Funciones para ir a cada frame
    def mainIr(self):
        self.stacked_widget.setCurrentIndex(0)

    def loginIr(self):
        self.stacked_widget.setCurrentIndex(1)



    # Funciones para validar antes de pasar al panel
    def panelIr(self):
        if self.stacked_widget.widget(1).TFUser.text()!='' and self.stacked_widget.widget(1).TFClave.text()!='':
            if  self.verificarClave() != False:
                    self.panel = PanelControl()
                    self.panel.show()
                    self.hide()
            else:
                self.msjAvrt("Datos incorrectos", "Clave o usuario incorrecto")
        else:
            self.msjAvrt("No hay datos", "por favor ingrese un dato para continuar")

    def msjAvrt(self, titulo, mensaje):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
   
            msg.setText(mensaje) #Aqui se configura el mensaje del messagebox
            msg.setWindowTitle(titulo)  #Aqui el titulo de la ventana del messagebox
            msg.setStandardButtons(QMessageBox.Ok)  #aqui se declaran los botones del messagebox
            retval = msg.exec_()   #esto inicia el messagebox no quitar xd

    def verificarUser(self): #Esta funcion verifica el usuario
        user=str(self.stacked_widget.widget(1).TFUser.text())#Asi se extrae los datos del texfield
        consulta2='Select Nombre From empleados where username= ?'
        parametros=(user,)
        row=consulta(consulta2,parametros).fetchall() #asi se haran las consultas a la bdd
        print(row)
        if row != []:
            print("Si esta en bdd")  #estos print indican si encontro a la persona en la bdd
            return True
        else:
            print("no esta en bdd") 
            return False
        
    def verificarClave(self):  #Esta funcion verifica la clave del usuario
        user=str(self.stacked_widget.widget(1).TFUser.text())   
        claveU=str(self.stacked_widget.widget(1).TFClave.text(),)
        #se hace la consulta a la bdd
        consul="SELECT Clave FROM Empleados WHERE Username=?"
        param=(user,)
        Clave=consulta(consul,param).fetchone()
        #Esto elimina caracteres que da la bdd
        Clave1=str(Clave)
        clave2=re.sub(",","",Clave1)
        clave3=re.sub("'","",clave2)
        clave4=re.sub("()","",clave3)
        Clavebd =re.sub("[()]","",clave4)
        #verifica la clave xd
        if user != [] and claveU != []:
            if claveU == Clavebd:
                print("Si esta en bdd")  #estos print indican si encontro a la persona en la bdd
                return True
            else:
                return False
        else:
            print("no esta en bdd") 
            return False 



# Inicio de la aplicacion
if __name__ == "__main__":
    # Crea la app de Pyqt5
    app = QApplication([])

    # Crea la instancia de nuestra ventana
    window = MainWindow()

    # Muestra la ventana
    window.show()

    # Ejecuta la app
    app.exec_()