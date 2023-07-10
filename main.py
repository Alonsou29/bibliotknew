import typing
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QMessageBox,QLineEdit
from PyQt5 import QtCore, uic
from panel import PanelControl
from conexion import consulta
import sys
import sqlite3
import re
from email.message import EmailMessage
import ssl
import smtplib
import random


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
        self.addFrame(r"frames\restablecer1.ui")
        self.addFrame(r"frames\restablecer2.ui")
        self.addFrame(r"frames\restablecer3.ui")


        # Te lleva al login al presionar el boton de inicio
        self.stacked_widget.widget(0).Inicio.clicked.connect(self.loginIr)

        # Te lleva al panel de control despues de ingresar el username y la clave
        self.stacked_widget.widget(1).Seguir.clicked.connect(self.panelIr)

        self.stacked_widget.widget(1).ClaveRevelar.stateChanged.connect(self.ver_password)

        # Te lleva a la primera pantalla de restablecer contraseña cuando se te ha olvidado
        self.stacked_widget.widget(1).Restablecer.clicked.connect(self.restablecer1Ir)

        # Te lleva a la segunda pantalla de restablecer contraseña despues de ingresar correo
        self.stacked_widget.widget(2).Seguir.clicked.connect(self.restablecer2Ir)

        # Te lleva a la tercera pantalla de restablecer contraseña despues de ingresar el codigo de verificacion
        self.stacked_widget.widget(3).Seguir.clicked.connect(self.restablecer3Ir)

        # Vuelve a enviar el codigo de verificacion en caso de que no haya llegado el correo
        self.stacked_widget.widget(3).Reenviar.clicked.connect(self.restablecerCorreo)

        # Te lleva al incio despues de poner una nueva clave
        self.stacked_widget.widget(4).Seguir.clicked.connect(self.restablecerClave)


        # Contador de veces que se escribio la clave de usuario incorrectamente
        self.contClave = 0

        # Variable que usaremos para codigos de verificacion en correos
        self.verifCode = 0

        # Variable para almacenar correo en caso de olvidar contraseña
        self.correoR = ""
    

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


    def restablecer1Ir(self):
        self.stacked_widget.widget(1).TFClave.setText("")
        self.stacked_widget.widget(1).TFUser.setText("")
        self.stacked_widget.setCurrentIndex(2)

    def restablecer2Ir(self):
        self.correoR = self.stacked_widget.widget(2).TFCorreo.text()
        # Verificar que correo esta en la bdd
        # Si esta hacer lo siguiente

        self.restablecerCorreo()
        self.stacked_widget.setCurrentIndex(3)

    # Funcion para comprobar que el codigo de verificacion de recuperar contraseña sea correcto
    def restablecer3Ir(self):
        codigo = self.stacked_widget.widget(3).TFCode.text()

        if codigo == str(self.verifCode):
            self.stacked_widget.setCurrentIndex(4)
        else:
            QMessageBox.critical(self, "Código Incorrecto", "Asegurese de ingresar el código correcto", QMessageBox.Ok)

    # Funcion para enviar correo con codigo de verificacion para recuperar contraseña
    def restablecerCorreo(self):
        # Creamos codigo de verificacion
        self.verifCode = random.randint(100000, 999999)

        # Mensaje del correo
        asuntoCorreo = "Restablecer contraseña"
        cuerpoCorreo = """Estimado usuario, se ha detectado un intento de restablecer contraseña. Para reestablecer su contraseña debe ingresar el código de verificación.

        Código de verificación:""" + str(self.verifCode) + """

        Si usted no ha intentado reestablecer su contraseña, puede ignorar este mensaje.

        Bibliotk Software"""
        # print(str(self.verifCode))
        self.enviarCorreo(self.correoR, asuntoCorreo, cuerpoCorreo)

    def restablecerClave(self):
        clave1 = self.stacked_widget.widget(4).TFClave.text()
        clave2 = self.stacked_widget.widget(4).TFClave_2.text()
        # Poner ojitos
        if clave1 == clave2:
            validado = self.validarClave(clave1)
            if validado:
                # cambia clave del usario con el correo self.correoR en la bdd
                asuntoCorreo = "Contaseña Reestablecida"
                cuerpoCorreo = """Estimado usuario, se le notifica que su contraseña ha sido restablecida exitosamente.
                Si usted no ha solicitado estos cambios por favor comuniquese con un administrador.

                Bibliotk Software"""
                self.enviarCorreo(self.correoR, asuntoCorreo, cuerpoCorreo)
                QMessageBox.question(self, 'Aviso' , "Cambios realizados exitosamente" , QMessageBox.Ok)
                self.mainIr()
            else:
                self.stacked_widget.widget(4).TFClave.setText("")
                self.stacked_widget.widget(4).TFClave_2.setText("")
        else:
            QMessageBox.critical(self, "Error", "Las contraseñas no coinciden", QMessageBox.Ok)

    # Funcion para validar la clave
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

    # Funcion para enviar correos
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

    # Funciones para validar antes de pasar al panel
    def panelIr(self):
        if self.stacked_widget.widget(1).TFUser.text()!='' and self.stacked_widget.widget(1).TFClave.text()!='':
            if  self.verificarClave() != False:
                    self.panel = PanelControl()
                    sql="SELECT idUsuario FROM Usuarios WHERE username=?"
                    user=str(self.stacked_widget.widget(1).TFUser.text())
                    param=(user,) 
                    dato=consulta(sql,param).fetchone()
                    Eliminar1=str(dato)
                    Eliminar2=re.sub(",","",Eliminar1)
                    Eliminar3=re.sub("'","",Eliminar2)
                    Eliminar4=re.sub("()","",Eliminar3)
                    vddfi =re.sub("[()]","",Eliminar4)
                    self.panel.usuario=vddfi
                    self.panel.show()
                    self.hide()
            else:
                self.contClave = self.contClave + 1

                if self.contClave != 3:
                    self.msjAvrt("Datos incorrectos", "Clave o usuario incorrecto")
                else:
                    self.msjAvrt("Datos incorrectos", "Acceso denegado. Por favor comuniquese con un administrador")
                    sys.exit()
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
        consulta2='Select Nombre From Usuarios where username= ?'
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
        consul="SELECT Clave FROM Usuarios WHERE Username=?"
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
        

    def ver_password(self): #Método para mostrar la contraseña cuando el checkbox está activo
        if self.stacked_widget.widget(1).ClaveRevelar.isChecked() == True:
            self.stacked_widget.widget(1).TFClave.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.stacked_widget.widget(1).TFClave.setEchoMode(QLineEdit.EchoMode.Password)


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