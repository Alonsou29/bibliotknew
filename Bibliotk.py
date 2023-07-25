import typing
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QMessageBox,QLineEdit
from PyQt5 import QtCore, uic, QtGui
from panel import PanelControl
from conexion import consulta
import sys
from sqlite3 import *
import re
from email.message import EmailMessage
import ssl
import smtplib
from socket import gaierror
from urllib.error import URLError
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

        # Ojitos de recuperar clave
        self.stacked_widget.widget(4).ClaveRevelar_3.stateChanged.connect(self.ver_claveNueva)

        self.stacked_widget.widget(4).ClaveRevelar_4.stateChanged.connect(self.ver_claveOtraVez)

        # Te lleva al incio despues de poner una nueva clave
        self.stacked_widget.widget(4).Seguir.clicked.connect(self.restablecerClave)

        # Botones de atras en restablecer clave
        self.stacked_widget.widget(2).atras.clicked.connect(self.atras1)
        self.stacked_widget.widget(3).atras.clicked.connect(self.atras2)
        self.stacked_widget.widget(4).atras.clicked.connect(self.atras3)


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


    def atras1(self):
        self.stacked_widget.widget(2).TFCorreo.setText("")
        self.mainIr()

    def atras2(self):
        ret = QMessageBox.question(self, 'Aviso' , "¿Seguro que desea regresar al inicio? El restablecimiento de contraseña se cancelará." , QMessageBox.Yes | QMessageBox.No)
        if ret == 16384:
            self.stacked_widget.widget(3).TFCode.setText("")
            self.mainIr()

    def atras3(self):
        ret = QMessageBox.question(self, 'Aviso' , "¿Seguro que desea regresar al inicio? El restablecimiento de contraseña se cancelará." , QMessageBox.Yes | QMessageBox.No)
        if ret == 16384:
            self.stacked_widget.widget(4).TFClave.setText("")
            self.stacked_widget.widget(4).TFClave_2.setText("")
            self.mainIr()


    def restablecer1Ir(self):
        self.stacked_widget.widget(1).TFClave.setText("")
        self.stacked_widget.widget(1).TFUser.setText("")
        self.stacked_widget.setCurrentIndex(2)

    def restablecer2Ir(self):
        self.correoR = self.stacked_widget.widget(2).TFCorreo.text()

        # Verifica que el correo ingresado este en la bdd
        sql="SELECT idUsuario FROM Usuarios WHERE UPPER(email)=UPPER(?) AND Activo=?"
        param=(self.correoR, "ACTIVO") 
        dato=consulta(sql,param).fetchone()
        Eliminar1=str(dato)
        Eliminar2=re.sub(",","",Eliminar1)
        Eliminar3=re.sub("'","",Eliminar2)
        Eliminar4=re.sub("()","",Eliminar3)
        idUser =re.sub("[()]","",Eliminar4)

        if idUser != "None":
            enviado = self.restablecerCorreo()
            if enviado:
                self.stacked_widget.widget(2).TFCorreo.setText("")
                self.stacked_widget.setCurrentIndex(3)
            else:
                self.stacked_widget.widget(2).TFCorreo.setText("")
                self.mainIr()
        else:
            QMessageBox.critical(self, "Aviso", "Este correo no pertenece a ningún usuario", QMessageBox.Ok)

    # Funcion para comprobar que el codigo de verificacion de recuperar contraseña sea correcto
    def restablecer3Ir(self):
        codigo = self.stacked_widget.widget(3).TFCode.text()

        if codigo == str(self.verifCode):
            self.stacked_widget.widget(3).TFCode.setText("")
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
        enviado = self.enviarCorreo(self.correoR, asuntoCorreo, cuerpoCorreo)

        if enviado:
            return True
        else:
            return False

    def restablecerClave(self):
        clave1 = self.stacked_widget.widget(4).TFClave.text()
        clave2 = self.stacked_widget.widget(4).TFClave_2.text()

        if clave1 == clave2:
            validado = self.validarClave(clave1)
            if validado:
                asuntoCorreo = "Contraseña Reestablecida"
                cuerpoCorreo = """Estimado usuario, se le notifica que su contraseña será reestablecida.
                Si usted no ha solicitado estos cambios por favor comuniquese con un administrador.

                Bibliotk Software"""
                enviado = self.enviarCorreo(self.correoR, asuntoCorreo, cuerpoCorreo)

                if enviado:
                    # Cambia clave del usario con el correo self.correoR en la bdd
                    sql="UPDATE Usuarios SET Clave=? WHERE UPPER(email)=UPPER(?)"
                    param=(clave1, self.correoR)
                    consulta(sql,param)
                    QMessageBox.question(self, 'Aviso' , "Cambios realizados exitosamente" , QMessageBox.Ok)
                    self.stacked_widget.widget(4).TFClave.setText("")
                    self.stacked_widget.widget(4).TFClave_2.setText("")
                    self.mainIr()
                else:
                    self.stacked_widget.widget(4).TFClave.setText("")
                    self.stacked_widget.widget(4).TFClave_2.setText("")
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
                QMessageBox.critical(self, "Aviso", "La contraseña debe tener letras mayusculas, minusculas, números y caracteres especiales", QMessageBox.Ok)
                return False
        else:
            QMessageBox.critical(self, "Aviso", "La contraseña debe tener entre 8 y 25 caracteres", QMessageBox.Ok)
            return False

    # Funcion para enviar correos
    def enviarCorreo(self, email_receptor, asunto, cuerpo):
        try:
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
        
            return True
        except (gaierror, URLError):
            QMessageBox.critical(self, "Error", "No se ha podido enviar el email debido a problemas de conexión, verifique su conexión a internet.")
            return False
        except smtplib.SMTPException as e:
            QMessageBox.critical(self, "Error", "Se ha presentado un error al enviar el email: " + e)
            return False

    # Funciones para validar antes de pasar al panel
    def panelIr(self):
        if self.stacked_widget.widget(1).TFUser.text()!='' and self.stacked_widget.widget(1).TFClave.text()!='':
            if  self.verificarClave() != False:
                    sql="SELECT idUsuario FROM Usuarios WHERE username=? OR email=?"
                    user=str(self.stacked_widget.widget(1).TFUser.text())
                    param=(user, user) 
                    dato=consulta(sql,param).fetchone()
                    Eliminar1=str(dato)
                    Eliminar2=re.sub(",","",Eliminar1)
                    Eliminar3=re.sub("'","",Eliminar2)
                    Eliminar4=re.sub("()","",Eliminar3)
                    vddfi =re.sub("[()]","",Eliminar4)
                    self.panel = PanelControl(vddfi)
                    self.panel.privilegios()
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
        consul="SELECT Clave FROM Usuarios WHERE (Username=? OR email=?) AND Activo=?"
        param=(user, user, "ACTIVO")
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
        
    # Ojito de login
    def ver_password(self): #Método para mostrar la contraseña cuando el checkbox está activo
        if self.stacked_widget.widget(1).ClaveRevelar.isChecked() == True:
            self.stacked_widget.widget(1).TFClave.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.stacked_widget.widget(1).TFClave.setEchoMode(QLineEdit.EchoMode.Password)

    # Ojito recuperar clave nueva
    def ver_claveNueva(self): #Método para mostrar la contraseña cuando el checkbox está activo
        if self.stacked_widget.widget(4).ClaveRevelar_3.isChecked() == True:
            self.stacked_widget.widget(4).TFClave.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.stacked_widget.widget(4).TFClave.setEchoMode(QLineEdit.EchoMode.Password)

    # Ojito recuperar clave otraves
    def ver_claveOtraVez(self): #Método para mostrar la contraseña cuando el checkbox está activo
        if self.stacked_widget.widget(4).ClaveRevelar_4.isChecked() == True:
            self.stacked_widget.widget(4).TFClave_2.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.stacked_widget.widget(4).TFClave_2.setEchoMode(QLineEdit.EchoMode.Password)

# Inicio de la aplicacion
if __name__ == "__main__":
    # Crea la app de Pyqt5
    app = QApplication([])

    # Crea la instancia de nuestra ventana
    window = MainWindow()
    window.setWindowIcon(QtGui.QIcon('bibliotk.png'))

    # Muestra la ventana
    window.show()

    # Ejecuta la app
    app.exec_()