import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox,QStackedWidget
from conexion import consulta
import re

class PanelControl(QMainWindow):

    def __init__(self):
        super().__init__()
        # Establece el titulo de la ventana
        #uic.loadUi("frames\diseño.ui",self)
        self.setWindowTitle("Bibliotk")

        # Establece el tamaño de la ventana y hace que no puedas cambiar su tamaño
        self.setFixedSize(800, 600) # (Ancho, Alto)

        # Crea instancia de QStackedWidget
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Crea y agrega frames al stacked widget
        self.addFrame("frames\panel.ui")
        

    def addFrame(self, ui_file):
        # Carga el archivo ui para el frame
        frame = uic.loadUi(ui_file)

        # Agrega el frame al stacked widget
        self.stacked_widget.addWidget(frame)
