import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox,QStackedWidget
from conexion import consulta
import re

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

        # Opciones del menubar
        self.panel.actionMostrarI.triggered.connect(self.inicioIrIr)
        self.panel.actionRegistrosC.triggered.connect(self.clientesIr)

    
    # Funciones del menubar
    def inicioIr(self):
        self.panel.stackedWidget.setCurrentIndex(0)

    def perfilIr(self):
        self.panel.stackedWidget.setCurrentIndex(1)

    def clientesIr(self):
        self.panel.stackedWidget.setCurrentIndex(2)

    def librosIr(self):
        self.panel.stackedWidget.setCurrentIndex(3)

    def autoresIr(self):
        self.panel.stackedWidget.setCurrentIndex(4)

    def prestamosIr(self):
        self.panel.stackedWidget.setCurrentIndex(5)

    def estadisticasIr(self):
        self.panel.stackedWidget.setCurrentIndex(6)

    def reportesIr(self):
        self.panel.stackedWidget.setCurrentIndex(7)

    def usuariosIr(self):
        self.panel.stackedWidget.setCurrentIndex(9)
