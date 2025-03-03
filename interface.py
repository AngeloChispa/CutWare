import cv2
import sys
import numpy as np
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import pyqtSignal, QSize
from PyQt6.QtWidgets import QHBoxLayout, QMessageBox
from main import *


class MiEtiqueta(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.Lista = []
        self.setStyleSheet("border: 1px solid black;")

class Window(QtWidgets.QWidget):

    def center(self):
        """
        Centra la Ventada SI o SI
        """
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __init__(self):
        super().__init__()
        self.OpenCV_image3 = None
        self.OpenCV_image = None
        self.OpenCV_image2 = None
        self.center()

        self._path = None

        self.viewer = MiEtiqueta()
        self.viewer2 = MiEtiqueta()
        self.viewer.setFixedSize(640, 480)
        self.viewer2.setFixedSize(640, 480)
        self.viewer.setScaledContents(True)
        self.viewer2.setScaledContents(True)

        self.buttonOpen = QtWidgets.QPushButton("Open Image")
        BUTTON_SIZE = QSize(200, 50)
        self.buttonOpen.setMinimumSize(BUTTON_SIZE)
        self.buttonOpen.clicked.connect(self.handleOpen)

        self.elements = []

        self.procesarImagenEntrada = QtWidgets.QPushButton("Procesar")
        self.procesarImagenEntrada.setMinimumSize(BUTTON_SIZE)
        self.procesarImagenEntrada.clicked.connect(self.ProcesarImage)

        self.guardarImagen = QtWidgets.QPushButton("Guardar")
        self.guardarImagen.setMinimumSize(BUTTON_SIZE)
        self.guardarImagen.clicked.connect(self.handleSaveFile)

        layout = QtWidgets.QGridLayout(self)
        self.botonProcesaReservado = QtWidgets.QPushButton("Buscar Señales de Trafico")
        self.botonProcesaReservado.setMinimumSize(BUTTON_SIZE)
        self.botonProcesaReservado.clicked.connect()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.buttonOpen)
        button_layout.addWidget(self.botonProcesaReservado)
        button_layout.addWidget(self.guardarImagen)

        layout.addLayout(button_layout, 0, 0, 1, 4)
        layout.addWidget(self.viewer, 1, 0, 1, 2)
        layout.addWidget(self.viewer2, 1, 2, 1, 2)

        Tamano = (self.viewer.size().width(), self.viewer.size().height())

        print(self.viewer.size(), type(self.viewer.size()), Tamano)

    def ProcesarImage(self):
        pass

    def handleSaveFile(self):
        if self.OpenCV_image2 is not None:
            defaultname = "example.png"

            fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", defaultname,
                                                                "Images(*.jpg *.png)")

            if fileName:
                if not fileName.endswith(('.png', '.jpg')):
                    fileName += ".png"
                cv2.imwrite(fileName, self.OpenCV_image2)
        else:
            QMessageBox.warning(self, "Error", "No hay nada que guardar aun")

    def handleOpen(self):
        start = "."

        path = QtWidgets.QFileDialog.getOpenFileName(self, "Choose File", start, "Images(*.jpg *.png)")[0]
        #self.FilePath = path + ".txt"
        if path:
            self._path = path
            self.ActualizarImagen()
        else:
            print("non") #añadir una advertencia que el path no vale verga



    def detectSigns(self):
        if self.OpenCV_image is None:
            QMessageBox.warning(self, "Error", "Aún no has cargado una imagen")
            return

        self.OpenCV_image2 = self.OpenCV_image.copy()
        hsv = cv2.cvtColor(self.OpenCV_image2, cv2.COLOR_BGR2HSV)


        self.ActualizarPixMap2(self.OpenCV_image2)

    def ActualizarPixMap(self):
        display_width = self.viewer.width()
        display_height = self.viewer.height()
        resized = cv2.resize(self.OpenCV_image3, (display_width, display_height), interpolation=cv2.INTER_LINEAR)
        QImageTemp = QtGui.QImage(
            cv2.cvtColor(resized, cv2.COLOR_BGR2RGB),
            resized.shape[1],
            resized.shape[0],
            resized.shape[1] * 3,
            QtGui.QImage.Format.Format_RGB888
        )
        self.viewer.setPixmap(QtGui.QPixmap(QImageTemp))

    def ActualizarPixMap2(self, image):
        display_width = self.viewer2.width()
        display_height = self.viewer2.height()
        resized_image = cv2.resize(image, (display_width, display_height), interpolation=cv2.INTER_LINEAR)
        qimage = QtGui.QImage(
            cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB),
            resized_image.shape[1],
            resized_image.shape[0],
            resized_image.shape[1] * 3,
            QtGui.QImage.Format.Format_RGB888
        )
        self.viewer2.setPixmap(QtGui.QPixmap(qimage))

    def ActualizarImagen(self):
        self.OpenCV_image = cv2.imread(self._path)
        self.OpenCV_image3 = self.OpenCV_image.copy()
        displaysize = (self.viewer.width(), self.viewer.height())
        self.OpenCV_image3 = cv2.resize(self.OpenCV_image3, displaysize, interpolation=cv2.INTER_LINEAR)
        QImageTemp = QtGui.QImage(
            cv2.cvtColor(self.OpenCV_image3, cv2.COLOR_BGR2RGB),
            self.OpenCV_image3.shape[1],
            self.OpenCV_image3.shape[0],
            self.OpenCV_image3.shape[1] * 3,
            QtGui.QImage.Format.Format_RGB888
        )
        pixmap = QtGui.QPixmap(QImageTemp)
        self.viewer.setPixmap(pixmap)
        self.viewer2.setPixmap(pixmap)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setWindowTitle("Traffic Sign Detector")
    window.show()
    sys.exit(app.exec())

