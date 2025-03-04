import sys
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QHBoxLayout, QMessageBox
from engine import *
from test import *

class MiEtiqueta(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.Lista = []
        self.setStyleSheet("border: 1px solid black;")

class Window(QtWidgets.QWidget):

    def center(self):
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
        self.viewer.setFixedSize(340, 580)
        self.viewer2.setFixedSize(340, 580)
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
        self.botonProcesaReservado = QtWidgets.QPushButton("Procesar imagen")
        self.botonProcesaReservado.setMinimumSize(BUTTON_SIZE)
        self.botonProcesaReservado.clicked.connect(self.detectImage)

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
            self.OpenCV_image = cv2.imread(path)
            if self.OpenCV_image is not None:
                height, width = self.OpenCV_image.shape[:2]

                if height > width:  # Vertical
                    label_width, label_height = 340, 580
                else:  # Horizontal
                    label_width, label_height = 580, 340

                self.viewer.setFixedSize(label_width, label_height)
                self.viewer2.setFixedSize(label_width, label_height)
            self.ActualizarImagen()
        else:
            print("El path no es valido, vuelva a intentar con otro") #añadir una advertencia que el path no vale verga

    #Alerta con la imagen para ver si es la que quiere el usuario
    def show_alert_with_image(self, image):
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle("Crop Image")
        msgBox.setText("¿Te parece bien este recorte? Sino puedes hacer tu propio recorte")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        height, width, channel = image.shape
        q_img = QtGui.QImage(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
            width,
            height,
            width * 3,
            QtGui.QImage.Format.Format_RGB888
        )

        pixmap = QtGui.QPixmap.fromImage(q_img)

        if width > height:
            msgBox.setIconPixmap(pixmap.scaled(400, 200))
        else:
            msgBox.setIconPixmap(pixmap.scaled(200, 400))
        respuesta = msgBox.exec()

        if respuesta == QMessageBox.StandardButton.Yes:
            return True
        else:
            return False

    def detectImage(self):
        if self.OpenCV_image is None:
            QMessageBox.warning(self, "Error", "Aún no has cargado una imagen")
            return

        self.OpenCV_image2 = self.OpenCV_image.copy()
        image = self.OpenCV_image.copy()

        height, width = image.shape[:2]
        if(height>width):
            image = cv2.resize(image, (500,1000))
        else:
            image = cv2.resize(image, (width*2,height*2))

        height, width = image.shape[:2]
        drawLines(image, height, width)

        processed_image = processImage(image)
        edged = recoverEdges(processed_image)
        list = contourList(edged)
        print(len(list))

        max = maxContour(list)
        #approx = tests(max)

        #cv2.imshow("Contornos", edged);

        #image = cv2.drawContours(image, [max.getContour()], -1, (0, 0, 255), 2)
        
        self.OpenCV_image2 = drawSquare(max.getContour(),image)

        self.ActualizarPixMap2(self.OpenCV_image2)
        crop = self.show_alert_with_image(self.OpenCV_image2.copy())

        if crop:
            print("Si le gustó siiiiiiiiiii")
        else:
            print("Pues que lo recorte el por quisquilloso")
            self.nuevaVentana(self._path)

    def nuevaVentana(self, path):
        self.ventana = ImageEditor(path)
        self.ventana.show()
        while self.ventana.isVisible():  # Espera hasta que la ventana de `ImageEditor` se cierre
            QApplication.processEvents()

        # Obtener la imagen recortada
        cropped_image = self.ventana.getCroppedImage()
        self.ActualizarPixMap2(cropped_image)

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

        display_size = (self.viewer.width(), self.viewer.height())
        self.OpenCV_image3 = cv2.resize(self.OpenCV_image3, display_size, interpolation=cv2.INTER_LINEAR)

        QImageTemp = QtGui.QImage(
            cv2.cvtColor(self.OpenCV_image3, cv2.COLOR_BGR2RGB),
            self.OpenCV_image3.shape[1],
            self.OpenCV_image3.shape[0],
            self.OpenCV_image3.shape[1] * 3,
            QtGui.QImage.Format.Format_RGB888
        )

        pixmap = QtGui.QPixmap(QImageTemp)
        self.viewer.setPixmap(pixmap)  # Solo actualizar la original


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setWindowTitle("Biggest Image Detector")
    window.show()
    sys.exit(app.exec())
