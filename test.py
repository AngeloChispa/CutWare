import sys
import cv2
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QPoint

class ImageEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.initUI()
    
    def getCroppedImage(self):
        return self.cropped_image
    
    def initUI(self):
        self.setWindowTitle("Dibujar Cuadrado")
        self.setGeometry(100, 100, 1000, 800)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
        self.image = None
        self.original_image = None
        self.drawing = False
        self.start_point = QPoint()
        self.end_point = QPoint()
    
        self.openImage()
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
    
    def openImage(self):
        self.image = cv2.imread(self.path)
        height, width = self.image.shape[:2]
        if height > width:
            self.image = cv2.resize(self.image,(400,800))
            self.offset = QPoint(291, 1)
        else:
            self.image = cv2.resize(self.image,(800,600)) 
            self.offset = QPoint(88, 88) 
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.original_image = self.image.copy()
        self.displayImage()
    
    
    def displayImage(self):
        if self.image is not None:
            height, width, channel = self.image.shape
            bytes_per_line = 3 * width
            qImg = QImage(self.image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            self.label.setPixmap(pixmap)
    
    def mousePressEvent(self, event):
        if self.image is not None and event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.image = self.original_image.copy()
            self.start_point = self.label.mapFromGlobal(event.globalPosition().toPoint()) - self.offset
            self.end_point = self.start_point
            self.displayImage()
    
    def mouseMoveEvent(self, event):
        if self.drawing and self.image is not None:
            self.end_point = self.label.mapFromGlobal(event.globalPosition().toPoint()) - self.offset
            self.image = self.original_image.copy()
            cv2.rectangle(self.image, (self.start_point.x(), self.start_point.y()), 
                          (self.end_point.x(), self.end_point.y()), (255, 0, 0), 2)
            self.displayImage()

    def show_alert_with_image(self, image):
        msgBox = QMessageBox();
        msgBox.setWindowTitle("Crop Image")
        msgBox.setText("¿Te parece bien este recorte? Sino puedes volver a hacerlo")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        height, width, channel = image.shape
        q_img = QImage(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
            width,
            height,
            width * 3,
            QImage.Format.Format_RGB888
        )

        pixmap = QPixmap.fromImage(q_img)

        if width > height:
            msgBox.setIconPixmap(pixmap.scaled(400, 200))
        else:
            msgBox.setIconPixmap(pixmap.scaled(200, 400))
        respuesta = msgBox.exec()

        if respuesta == QMessageBox.StandardButton.Yes:
            return True
        else:
            return False
    
    def mouseReleaseEvent(self, event):
        if self.drawing and self.image is not None:
            self.drawing = False
            self.end_point = self.label.mapFromGlobal(event.globalPosition().toPoint()) - self.offset
            print(self.end_point)
            self.image = self.original_image.copy()
            cv2.rectangle(self.image, (self.start_point.x(), self.start_point.y()),
                          (self.end_point.x(), self.end_point.y()), (255, 0, 0), 2)
            self.displayImage()
            x1, y1 = self.start_point.x(), self.start_point.y()
            x2, y2 = self.end_point.x(), self.end_point.y()

            # Asegurarse de que las coordenadas son válidas (evitar índices negativos o fuera de rango)
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            showImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            # Extraer la subimagen (área seleccionada dentro del rectángulo)
            self.cropped_image = self.original_image[y1:y2, x1:x2]
            self.cropped_image = cv2.cvtColor(self.cropped_image, cv2.COLOR_BGR2RGB)
            # Mostrar o guardar la subimagen (opcional)
            crop = self.show_alert_with_image(self.cropped_image)

            if crop:
                self.close()

