import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap

image_list = os.listdir('./Images')
current_image = image_list[0]
back_image_ = image_list[-1]

class InspectionWindow(QMainWindow):
    def __init__(self):
        super(InspectionWindow, self).__init__()
        loadUi('Image Swapping.ui', self)
        self.previous_button.clicked.connect(self.previous_image)
        self.next_button.clicked.connect(self.next_image)
        self.enter_button.clicked.connect(self.enter_image)
        self.back_button.clicked.connect(self.back_image)
        self.current_image = current_image
        self.back_image_ = back_image_

    def previous_image(self):
        self.back_image_ = self.current_image
        self.current_image = image_list[(image_list.index(self.current_image) - 1) % len(image_list)]
        pixmap = QPixmap('./Images/' + self.current_image)
        self.label.setPixmap(pixmap)
        

    def next_image(self):
        self.back_image_ = self.current_image
        self.current_image = image_list[(image_list.index(self.current_image) + 1) % len(image_list)]
        pixmap = QPixmap('./Images/' + self.current_image)
        self.label.setPixmap(pixmap)
        

    def enter_image(self):
        self.code = self.line_input.text()
        if int(self.code) in list(range(1, len(image_list) + 1)):
            self.back_image_ = self.current_image
            self.current_image = image_list[int(self.code) - 1]
            pixmap = QPixmap('./Images/' + self.current_image)

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Enter from 1 to {}'.format(len(image_list)))
            x=msg.exec_()
        self.label.setPixmap(pixmap)
        

    def back_image(self):
        print(self.back_image_)
        pixmap = QPixmap('./Images/' + self.back_image_)
        self.label.setPixmap(pixmap)
        self.back_image_, self.current_image = self.current_image, self.back_image_


app = QApplication(sys.argv)
mainwindow = InspectionWindow()
mainwindow.show()
sys.exit(app.exec_())
print()
