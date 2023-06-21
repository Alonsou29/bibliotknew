import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox
from conexion import conec
import MySQLdb
import re

class PanelControl(QMainWindow):

    def __init__(self):
        super().__init__()
