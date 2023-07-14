from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow

class Clientes(QMainWindow):

    def __init__(self):
        super().__init__()

        self.client = uic.loadUi("frames\SeleccionarC.ui",self)

        # Establece titulo de la ventana
        self.client.setWindowTitle("Seleccione Clientes")
        self.client.setWindowIcon(QtGui.QIcon('logo.png'))
        # Establece el tamaño de la ventana y hace que no puedas cambiar su tamaño
        self.client.setFixedSize(800, 600) # (Ancho, Alto)