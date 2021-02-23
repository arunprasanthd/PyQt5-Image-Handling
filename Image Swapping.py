'''
Program to view images from a specified folder using PyQt5 and QtDesigner
Features: Previous, Next, Enter, Back, Dynamic images & push button, for creation & operation
'''
# To import needed modules such as sys, os & PyQt5 and their classes
import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QGroupBox, QMainWindow, QPushButton, QMessageBox, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap

# To select images folder
path_ = './Images/'
image_list = os.listdir(path_)
current_image = image_list[0]
back_image_ = image_list[-1]


# Class to create scroll widget
class Window(QWidget):
    def __init__(self):
        super().__init__()
        formLayout = QFormLayout()
        groupBox = QGroupBox("This Is Group Box")
        self.labelList = []
        self.buttonList = []
        self.image_list = image_list
        for i in range(len(image_list)):
            self.image_ = QLabelClickable()
            self.button_ = QPushButton(str(i + 1))
            self.pixmap = QPixmap(path_ + self.image_list[i])
            self.image_.setPixmap(self.pixmap)
            self.image_.setScaledContents(True)
            self.image_.setFixedHeight(100)
            self.image_.setFixedWidth(100)
            self.button_.setFixedHeight(30)
            self.button_.setFixedWidth(30)
            self.labelList.append(self.image_)
            self.buttonList.append(self.button_)
            formLayout.addRow(self.buttonList[i], self.labelList[i])
        groupBox.setLayout(formLayout)
        scroll = QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        self.show()


# Class to create clickable label
class QLabelClickable(QLabel):
    clicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)

    def mousePressEvent(self, event):
        self.ultimo = "Clic"

    def mouseReleaseEvent(self, event):
        if self.ultimo == "Clic":
            self.clicked.emit(self.ultimo)

    def performSingleClickAction(self):
        if self.ultimo == "Clic":
            self.clicked.emit(self.ultimo)


# Class to create object for Main Window
class InspectionWindow(QMainWindow):
    def __init__(self):
        # To inherit all the attributes and methods from parent class QMainWindow
        super(InspectionWindow, self).__init__()

        # To load .ui file into class InspectionWindow
        loadUi('Image Swapping1.ui', self)

        self.new_win = Window()
        self.verticalLayout.addWidget(self.new_win)

        self.image_list = image_list
        self.current_image = current_image
        self.back_image_ = back_image_
        self.line_input.setPlaceholderText('Enter from 1 to {}'.format(len(self.image_list)))
        self.button_list = []
        pixmap = QPixmap(path_ + self.image_list[0])
        self.label.setPixmap(pixmap)

        # To perform pushbutton clicking operations to change image
        self.previous_button.clicked.connect(self.previous_image)
        self.next_button.clicked.connect(self.next_image)
        self.enter_button.clicked.connect(self.enter_image)
        self.back_button.clicked.connect(self.back_image)

        # To perform corresponding pushbutton clicking operations to view image
        for c, d in zip(self.new_win.buttonList, self.image_list):
            c.clicked.connect(lambda xy, d=d: self.click_button(d))

        # To perform corresponding thumbnail clicking operations to view image
        for e, f in zip(self.new_win.labelList, self.image_list):
            e.clicked.connect(lambda xy, f=f: self.click_button(f))

    # Method to view corresponding image of clicked button
    def click_button(self, a):
        self.back_image_ = self.current_image
        self.current_image = a
        pixmap = QPixmap(path_ + self.current_image)
        self.label.setPixmap(pixmap)

    # Method to view previous image
    def previous_image(self):
        self.back_image_ = self.current_image
        self.current_image = self.image_list[(self.image_list.index(self.current_image) - 1) % len(self.image_list)]
        pixmap = QPixmap(path_ + self.current_image)
        self.label.setPixmap(pixmap)

    # Method to view next image
    def next_image(self):
        self.back_image_ = self.current_image
        self.current_image = self.image_list[(self.image_list.index(
            self.current_image) + 1) % len(self.image_list)]
        pixmap = QPixmap(path_ + self.current_image)
        self.label.setPixmap(pixmap)

    # Method to view corresponding image of entered number
    def enter_image(self):
        self.code = self.line_input.text()
        if self.code.isnumeric() and int(self.code) in list(range(1, len(self.image_list) + 1)):
            self.back_image_ = self.current_image
            self.current_image = self.image_list[int(self.code) - 1]
            pixmap = QPixmap(path_ + self.current_image)
            self.label.setPixmap(pixmap)
        # Error pop-up for blank input, input number out of range and non-integer input
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Enter from 1 to {}'.format(len(image_list)))
            x = msg.exec_()
        self.line_input.clear()

    # Method to view back image
    def back_image(self):
        pixmap = QPixmap(path_ + self.back_image_)
        self.label.setPixmap(pixmap)
        self.back_image_, self.current_image = self.current_image, self.back_image_


# To show and exit the GUI window
app = QApplication(sys.argv)
mainwindow = InspectionWindow()
mainwindow.show()
sys.exit(app.exec_())
