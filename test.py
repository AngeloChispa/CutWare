import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, QPoint

class ImageEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Dibujar Cuadrado")
        self.setGeometry(100, 100, 800, 600)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btnOpen = QPushButton("Abrir Imagen", self)
        self.btnOpen.clicked.connect(self.openImage)
        
        layout = QVBoxLayout()
        layout.addWidget(self.btnOpen)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.image = None
        self.original_image = None
        self.drawing = False
        self.start_point = QPoint()
        self.end_point = QPoint()
        
    def openImage(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image = cv2.imread(file_path)
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
            self.start_point = event.position().toPoint()
    
    def mouseMoveEvent(self, event):
        if self.drawing and self.image is not None:
            self.end_point = event.position().toPoint()
            self.image = self.original_image.copy()
            cv2.rectangle(self.image, (self.start_point.x(), self.start_point.y()), 
                          (self.end_point.x(), self.end_point.y()), (255, 0, 0), 2)
            self.displayImage()
    
    def mouseReleaseEvent(self, event):
        if self.drawing and self.image is not None:
            self.drawing = False
            self.end_point = event.position().toPoint()
            self.image = self.original_image.copy()
            cv2.rectangle(self.image, (self.start_point.x(), self.start_point.y()), 
                          (self.end_point.x(), self.end_point.y()), (255, 0, 0), 2)
            self.original_image = self.image.copy()
            self.displayImage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageEditor()
    window.show()
    sys.exit(app.exec())
