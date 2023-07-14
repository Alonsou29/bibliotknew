from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow

class Autores(QMainWindow):

    def __init__(self):
        super().__init__()

        self.autor = uic.loadUi("frames\SeleccionarA.ui",self)

        # Establece titulo de la ventana
        self.autor.setWindowTitle("Seleccione Autores")
        self.autor.setWindowIcon(QtGui.QIcon('logo.png'))
        # Establece el tamaño de la ventana y hace que no puedas cambiar su tamaño
        self.autor.setFixedSize(800, 600) # (Ancho, Alto)