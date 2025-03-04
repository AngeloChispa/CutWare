import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
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
        self.image = cv2.imread("meme.jpg")
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.original_image = self.image.copy()
        self.resizeWindowToImage()
        self.displayImage()
    
    def resizeWindowToImage(self):
        if self.image is not None:
            height, width, _ = self.image.shape
            max_width, max_height = 1080, 1200
            new_width = min(width + 20, max_width)
            new_height = min(height + 80, max_height)
            self.resize(new_width, new_height)
    
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
            self.start_point = self.label.mapFromGlobal(event.globalPosition().toPoint())
            self.end_point = self.start_point
            self.displayImage()
    
    def mouseMoveEvent(self, event):
        if self.drawing and self.image is not None:
            self.end_point = self.label.mapFromGlobal(event.globalPosition().toPoint())
            self.image = self.original_image.copy()
            cv2.rectangle(self.image, (self.start_point.x(), self.start_point.y()), 
                          (self.end_point.x(), self.end_point.y()), (255, 0, 0), 2)
            self.displayImage()
    
    def mouseReleaseEvent(self, event):
        if self.drawing and self.image is not None:
            self.drawing = False
            self.end_point = self.label.mapFromGlobal(event.globalPosition().toPoint())
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
