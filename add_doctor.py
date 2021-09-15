import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
from PIL import Image


con = sqlite3.connect("Hospital_database.db")
cur = con.cursor()

DefaultImg = "man.png"


class AddDoctor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Doctor")
        self.setGeometry(350,150,400,600)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon('icons/logo.png'))

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.titleText = QLabel("New Doctor")
        self.titleText.setAlignment(Qt.AlignCenter)
        self.doctorImg = QLabel()
        self.img = QPixmap("doctor_imgs/man.png")
        self.doctorImg.setPixmap(self.img)
        self.doctorImg.setAlignment(Qt.AlignCenter)

        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter Doctor's name")
        self.mobEntry = QLineEdit()
        self.mobEntry.setPlaceholderText("Enter Mob. No.")
        self.addressEntry = QTextEdit()
        self.addressEntry.setPlaceholderText("Enter Address")
        self.DoctorStatus = QComboBox()
        self.DoctorStatus.addItems(["Available","Not Available"])
        self.uploadBtn = QPushButton("Upload Image")
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.submitDoctorInfo)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout  = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.doctorImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Name: "),self.nameEntry)
        self.bottomLayout.addRow(QLabel("Mob. No: "),self.mobEntry)
        self.bottomLayout.addRow(QLabel("Address: "),self.addressEntry)
        self.bottomLayout.addRow(QLabel("Status: "),self.DoctorStatus)
        self.bottomLayout.addRow(QLabel("Image: "),self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""),self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def uploadImg(self):
        global DefaultImg
        size = (256, 256)
        self.filename, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image files (*.jpg *.png *.jpeg)")
        if ok:
            DefaultImg = os.path.basename(self.filename)
            Img = Image.open(self.filename)
            Img = Img.resize(size)
            Img.save("doctor_imgs/{0}".format(DefaultImg))

    def submitDoctorInfo(self):
        global DefaultImg
        name = self.nameEntry.text()
        mob = self.mobEntry.text()
        address = self.addressEntry.toPlainText()
        # status = self.DoctorStatus.currentText()

        if(name and mob and address !=""):
            try:
                query =("INSERT INTO 'doctors' (doctor_name,doctor_phone,doctor_img,doctor_address) VALUES (?,?,?,?)")
                cur.execute(query,(name,mob,DefaultImg,address))
                con.commit()
                QMessageBox.information(self,"Info","Doctor has been Added")
            except:
                QMessageBox.information(self,"Info","Doctor has not been Added")
        else:
            QMessageBox.information(self, "Warning", "Fields cannot be Empty")
