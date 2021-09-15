import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image
import sqlite3


DefaultImg = "xyz.png"
con = sqlite3.connect("Hospital_database.db")
cur = con.cursor()
now = QDateTime.currentDateTime()
dt = now.toString(Qt.ISODate)

last = cur.execute("SELECT * FROM patients").fetchall()[-1]
reg_Id = last[1]+1
# print(reg_Id)

class AddPatient(QWidget):
    def __init__(self):
        super().__init__()
        #########Initailising Window###################
        self.setWindowTitle("New Registration")
        self.setGeometry(300, 150, 700, 620)
        self.setFixedSize(self.size()) # Fixed size of window
        self.setWindowIcon(QIcon("icons/logo.png"))

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()


    def widgets(self):
        self.addPatientImg = QLabel()
        self.img = QPixmap('icons/xyz.png')
        self.addPatientImg.setPixmap(self.img)
        self.addPatientImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("New Patient")
        self.titleText.setAlignment(Qt.AlignCenter)

        ##########################################################
        global reg_Id
        self.regText = QLabel("Registration Id: ")
        self.regEntry = QLineEdit()
        self.regEntry.setFixedWidth(80)
        self.regEntry.setText(str(reg_Id))
        self.dateTimeText = QLabel("Date & Time: ")
        self.dateTimeText.setFixedWidth(160)
        self.dateTimeEntry = QLineEdit()
        self.dateTimeEntry.setFixedWidth(140)
        self.dateTimeEntry.setText(dt)
        ###########################################################

        self.nameText =QLabel("Patient Name: ")
        self.namePrefix = QComboBox()
        self.namePrefix.setFixedWidth(50)
        self.namePrefix.addItems(["Mr.","Mrs."])
        self.FnameEntry = QLineEdit()
        self.FnameEntry.setFixedWidth(150)
        self.FnameEntry.setPlaceholderText("Enter First Name")
        self.LnameEntry = QLineEdit()
        self.LnameEntry.setFixedWidth(150)
        self.LnameEntry.setPlaceholderText("Enter Last Name")
        ############################################################

        self.ageText = QLabel("Age: ")
        self.ageEntry = QLineEdit()
        self.ageEntry.setPlaceholderText("Enter Age")
        self.sexText = QLabel("Sex: ")
        self.sexCombo = QComboBox()
        self.sexCombo.setFixedWidth(60)
        self.sexCombo.addItems(["Male","Female","Others"])
        #############################################################
        self.addressText = QLabel("Address: ")
        self.addressEntry  = QLineEdit()
        self.addressEntry.setFixedWidth(220)
        self.addressEntry.setPlaceholderText("Enter Address")
        self.districtText = QLabel("District")
        districts = ["Ahmednagar", "Akola", "Amravati", "Aurangabad", "Beed", "Bhandara", "Buldhana", "Chandrapur",
                     "Dhule", "Gadchiroli", "Gondia", "Hingoli", "Jalgaon", "Jalna", "Kolhapur", "Latur",
                     "Mumbai City", "Mumbai Suburban", "Nagpur", "Nanded", "Nandurbar", "Nashik", "Osmanabad",
                     "Palghar", "Parbhani", "Pune",
                     "Raigad", "Ratnagiri", "Sangli", "Satara", "Sindhudurg", "Solapur", "Thane", "Wardha", "Washim",
                     "Yavatmal"]
        self.districtCombo = QComboBox()
        self.districtCombo.setFixedWidth(100)
        for dis in districts:
            self.districtCombo.addItem(dis)
        self.talukaText = QLabel("Taluka: ")
        self.talukaEntry = QLineEdit()

        ##################################################
        self.occupationText = QLabel("Occupation: ")
        self.occupationEntry = QComboBox()
        self.occupationEntry.addItems(["Farmer","Student","Self","Teacher","Gov. Service","Pvt. Service","Engg.","Doctor"])
        self.phoneText = QLabel("Mob. No.: ")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter Phone")
        ##################################################
        self.imgText = QLabel("Image: ")
        self.imguploadBtn = QPushButton("Upload")
        self.imguploadBtn.clicked.connect(self.uploadImg)

        self.referredText = QLabel("Referred by: ")
        self.referredEntry = QComboBox()
        self.referredEntry.setFixedWidth(120)

        self.submitBtn = QPushButton("Submit")
        self.submitBtn.clicked.connect(self.addPatientData)





    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QGridLayout()
        # self.bottomLayout.setVerticalSpacing(20)
        # self.bottomLayout.setHorizontalSpacing(5)

        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.addPatientImg)
        self.topFrame.setLayout(self.topLayout)
        ############### HBox1 ##########################
        self.bottomLayout.addWidget(self.regText,0,0)
        self.bottomLayout.addWidget(self.regEntry,0,1)
        self.bottomLayout.addWidget(self.dateTimeText,0,2)
        self.bottomLayout.addWidget(self.dateTimeEntry,0,3)
        #####################hbox2##########################
        self.bottomLayout.addWidget(self.nameText,1,0)
        self.bottomLayout.addWidget(self.namePrefix)
        self.bottomLayout.addWidget(self.FnameEntry)
        self.bottomLayout.addWidget(self.LnameEntry)
        #######################hbox3########################
        self.bottomLayout.addWidget(self.sexText,2,0)
        self.bottomLayout.addWidget(self.sexCombo,2,1)
        self.bottomLayout.addWidget(self.ageText,2,2)
        self.bottomLayout.addWidget(self.ageEntry,2,3)
        ######################hbox3#########################
        self.bottomLayout.addWidget(self.addressText,3,0)
        self.bottomLayout.addWidget(self.addressEntry)
        #######################hbox4#########################
        self.bottomLayout.addWidget(self.districtText,4,0)
        self.bottomLayout.addWidget(self.districtCombo,4,1)
        self.bottomLayout.addWidget(self.talukaText,4,2)
        self.bottomLayout.addWidget(self.talukaEntry,4,3)
        #################### hbox5###########################
        self.bottomLayout.addWidget(self.occupationText,5,0)
        self.bottomLayout.addWidget(self.occupationEntry,5,1)
        self.bottomLayout.addWidget(self.phoneText,5,2)
        self.bottomLayout.addWidget(self.phoneEntry,5,3)
        #######################################################
        self.bottomLayout.addWidget(self.imgText,6,0)
        self.bottomLayout.addWidget(self.imguploadBtn,6,1)
        self.bottomLayout.addWidget(self.referredText,6,2)
        self.bottomLayout.addWidget(self.referredEntry,6,3)
        ################ End box ############################
        self.bottomLayout.addWidget(self.submitBtn,7,3)
        #########################################################

        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame,35)
        self.mainLayout.addWidget(self.bottomFrame,65)
        self.setLayout(self.mainLayout)

    def uploadImg(self):
        global DefaultImg
        size = (256,256)
        self.filename,ok = QFileDialog.getOpenFileName(self,"Upload Image","","Image files (*.jpg *.png *.jpeg)")
        if ok:
            DefaultImg = os.path.basename(self.filename)
            Img = Image.open(self.filename)
            Img = Img.resize(size)
            Img.save("patients_imgs/{0}".format(DefaultImg))

    def addPatientData(self):
        global DefaultImg,reg_Id
        regId = self.regEntry.text()
        time = self.dateTimeEntry.text()
        name = self.namePrefix.currentText() + " " + self.FnameEntry.text() + " " + self.LnameEntry.text()
        sex = self.sexCombo.currentText()
        age = self.ageEntry.text()
        address = self.addressEntry.text()
        district = self.districtCombo.currentText()
        taluka = self.talukaEntry.text()
        occupation = self.occupationEntry.currentText()
        phone = self.phoneEntry.text()
        refer = self.referredEntry.currentText()

        if(name and phone and address and regId !=""):
            try:
                query = ("INSERT INTO 'patients' (registration_id,date_time,patient_name,patient_phone,patient_age,patient_sex,patient_address,district,taluka,occupation,patient_img,referred_by) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)")
                cur.execute(query,(regId,time,name,phone,age,sex,address,district,taluka,occupation,DefaultImg,refer))
                con.commit()
                QMessageBox.information(self,"Info","Patient has been Added")
                # reg_Id = reg_Id+1



            except:
                QMessageBox.information(self,"Info","Patient has not been Added")
        else:
            QMessageBox.information(self,"Warning","Fields cannot be empty")







