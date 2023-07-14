from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow

class Libros(QMainWindow):

    def __init__(self):
        super().__init__()

        self.libro = uic.loadUi("frames\SeleccionarL.ui",self)

        # Establece titulo de la ventana
        self.libro.setWindowTitle("Seleccione Libros")
        self.libro.setWindowIcon(QtGui.QIcon('logo.png'))
        # Establece el tamaño de la ventana y hace que no puedas cambiar su tamaño
        self.libro.setFixedSize(800, 600) # (Ancho, Alto)