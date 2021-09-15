import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image
import sqlite3
import add_patient,add_doctor,style

con = sqlite3.connect("Hospital_database.db")
cur = con.cursor()
now = QDateTime.currentDateTime()
dt = now.toString(Qt.ISODate)



class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        #########Initailising Window###################
        self.setWindowTitle("Hospital Management")
        self.setGeometry(300, 150, 1550, 850)
        # self.setFixedSize(self.size()) # Fixed size of window
        self.setWindowIcon(QIcon("icons/logo.png"))

        self.UI()
        self.show()

    def UI(self):
        # self.setStyleSheet("font-size: 14px;")
        self.toolbar()
        self.tabbar()
        self.widgets()
        self.layouts()
        self.displayPatient()
        self.displayDoctors()

    def toolbar(self):
        ################ adding tool bar ##############
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(Qt.LeftToolBarArea,self.tb) # adding tool bar to the left sife

        ################ adding New Patient icon ##################
        self.newPatient = QAction(QIcon("icons/old.png"),"NEW PATIENT",self)
        self.tb.addAction(self.newPatient)
        self.tb.addSeparator()
        self.newPatient.triggered.connect(self.fucnNewPatient)


        ############### Adding Doctor icon ##########################
        self.addDoctor = QAction(QIcon("icons/member.png"),"ADD DOCTOR",self)
        self.tb.addAction(self.addDoctor)
        self.tb.addSeparator()
        self.addDoctor.triggered.connect(self.funcAddDoctor)

        self.statistics = QAction(QIcon("icons/stat.png"),"Statistics",self)
        self.tb.addAction(self.statistics)
        self.tb.addSeparator()






    def tabbar(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        self.tabs.addTab(self.tab1, "Patients")
        self.tabs.addTab(self.tab2, "Doctors")
        self.tabs.addTab(self.tab3, "Appointment")
        self.tabs.addTab(self.tab4, "View")


    def widgets(self):
        ################### Left layout widgets #################
        self.patientTable = QTableWidget()
        # self.patientTable.setMouseTracking(True)
        self.patientTable.setColumnCount(14)
        self.patientTable.setColumnHidden(0,True)

        ################ Adding Patient table info ###############
        self.patientTable.setHorizontalHeaderItem(0,QTableWidgetItem("Patient Id"))
        self.patientTable.setHorizontalHeaderItem(1,QTableWidgetItem("Registration Id"))
        self.patientTable.setHorizontalHeaderItem(2,QTableWidgetItem("Date & Time"))
        self.patientTable.setHorizontalHeaderItem(3,QTableWidgetItem("Patient Name"))
        self.patientTable.setHorizontalHeaderItem(4,QTableWidgetItem("Patient Phone"))
        self.patientTable.setHorizontalHeaderItem(5,QTableWidgetItem("Age"))
        self.patientTable.setHorizontalHeaderItem(6,QTableWidgetItem("Sex "))
        self.patientTable.setHorizontalHeaderItem(7,QTableWidgetItem("Illness"))
        self.patientTable.setHorizontalHeaderItem(8,QTableWidgetItem("Patient Address"))
        self.patientTable.setHorizontalHeaderItem(9,QTableWidgetItem("District"))
        self.patientTable.setHorizontalHeaderItem(10,QTableWidgetItem("Taluka"))
        self.patientTable.setHorizontalHeaderItem(11,QTableWidgetItem("Occupation"))
        self.patientTable.setHorizontalHeaderItem(12,QTableWidgetItem("Referred by"))
        self.patientTable.setHorizontalHeaderItem(13,QTableWidgetItem("Appointment"))
        self.patientTable.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.patientTable.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeToContents)
        self.patientTable.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeToContents)
        self.patientTable.horizontalHeader().setSectionResizeMode(5,QHeaderView.ResizeToContents)
        self.patientTable.horizontalHeader().setSectionResizeMode(6,QHeaderView.ResizeToContents)
        self.patientTable.horizontalHeader().setSectionResizeMode(13,QHeaderView.ResizeToContents)

        self.patientTable.doubleClicked.connect(self.SelectedPatient)

        self.searchText = QLabel("Search")
        self.searchEntry = QLineEdit()
        self.searchEntry.setPlaceholderText("Search by Reg. Id or Mob. No.")
        self.searchBtn = QPushButton("Search")
        self.searchBtn.clicked.connect(self.SearchPatient)

        self.allpatients = QRadioButton("All Patients")
        self.appointmentPatients = QRadioButton("Appointment")
        self.notAppointmentPatients = QRadioButton("Non Appointments")
        self.showBtn = QPushButton("Show")
        self.showBtn.clicked.connect(self.listPatients)

        self.doctorsTable = QTableWidget()
        self.doctorsTable.setColumnCount(5)
        self.doctorsTable.setColumnHidden(0, True)

        self.doctorsTable.setHorizontalHeaderItem(0, QTableWidgetItem("Doctor Id"))
        self.doctorsTable.setHorizontalHeaderItem(1, QTableWidgetItem("Doctor Name"))
        self.doctorsTable.setHorizontalHeaderItem(2, QTableWidgetItem("Mob. No."))
        self.doctorsTable.setHorizontalHeaderItem(3, QTableWidgetItem("Address"))
        self.doctorsTable.setHorizontalHeaderItem(4, QTableWidgetItem("Status"))
        self.doctorsTable.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.doctorsTable.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        self.doctorsTable.horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch)
        self.doctorsTable.horizontalHeader().setSectionResizeMode(4,QHeaderView.Stretch)
        self.doctorsTable.doubleClicked.connect(self.SelectedDoctor)

        self.doctorSearchText = QLabel("Search")
        self.dotorSearchEntry = QLineEdit()
        self.dotorSearchEntry.setPlaceholderText("Search For Doctors")
        self.doctorSearchBtn = QPushButton("Search")
        self.doctorSearchBtn.clicked.connect(self.SearchDoctor)

        self.allDoctors = QRadioButton("All Doctors")
        self.availableDoctors = QRadioButton("Available")
        self.notAvailableDoctors = QRadioButton("Not Available")
        self.doctorShowBtn = QPushButton("Show")
        self.doctorShowBtn.clicked.connect(self.listDoctors)

        ####################### Appointment Section ##########################
        self.appointmentTable = QTableWidget()
        self.appointmentTable.setColumnCount(6)
        self.appointmentTable.setColumnHidden(0,True)

        self.appointmentTable.setHorizontalHeaderItem(0,QTableWidgetItem("Appointment Id"))
        self.appointmentTable.setHorizontalHeaderItem(1,QTableWidgetItem("Registration Id"))
        self.appointmentTable.setHorizontalHeaderItem(2,QTableWidgetItem("Patient Name"))
        self.appointmentTable.setHorizontalHeaderItem(3,QTableWidgetItem("Doctor Name"))
        self.appointmentTable.setHorizontalHeaderItem(4,QTableWidgetItem("Test Name"))
        self.appointmentTable.setHorizontalHeaderItem(5,QTableWidgetItem("Date and Time"))




    def layouts(self):
        ########### Creating layout ##################
        self.mainLayout = QHBoxLayout()
        self.mainRightLayout = QVBoxLayout()
        self.mainLeftLayout = QVBoxLayout()

        self.rightTopLayout = QHBoxLayout()
        self.rightMiddleLayout = QHBoxLayout()

        self.rightTopGroupBox = QGroupBox("Search For Patients")
        self.rightTopGroupBox.setStyleSheet(style.searhBoxStyle())
        self.rightMiddleGroupBox = QGroupBox("List Box")
        self.rightMiddleGroupBox.setStyleSheet(style.listBoxStyle())
        self.rightBottomGroupBox = QGroupBox()

        ################# Adding Widgets into Layout ##################
        self.mainLeftLayout.addWidget(self.patientTable)
        self.mainLayout.addLayout(self.mainLeftLayout, 70)

        self.rightTopLayout.addWidget(self.searchText)
        self.rightTopLayout.addWidget(self.searchEntry)
        self.rightTopLayout.addWidget(self.searchBtn)
        self.rightTopGroupBox.setLayout(self.rightTopLayout)

        self.rightMiddleLayout.addWidget(self.allpatients)
        self.rightMiddleLayout.addWidget(self.appointmentPatients)
        self.rightMiddleLayout.addWidget(self.notAppointmentPatients)
        self.rightMiddleLayout.addWidget(self.showBtn)
        self.rightMiddleGroupBox.setLayout(self.rightMiddleLayout)

        self.mainRightLayout.addWidget(self.rightTopGroupBox,20)
        self.mainRightLayout.addWidget(self.rightMiddleGroupBox,20)
        self.mainRightLayout.addWidget(self.rightBottomGroupBox,60)
        self.mainLayout.addLayout(self.mainRightLayout, 30)

        self.tab1.setLayout(self.mainLayout)
        ################################# TAB2 ##############################

        self.doctorMainLayout = QHBoxLayout()
        self.doctormainRightLayout = QVBoxLayout()
        self.doctormainLeftLayout = QHBoxLayout()

        self.doctorRightTopLayout = QHBoxLayout()
        self.doctorRightMiddleLayout = QHBoxLayout()

        self.doctorRightTopGroupBox = QGroupBox("Search For Doctors")
        self.doctorRightTopGroupBox.setStyleSheet(style.searhBoxStyleDoctor())
        self.doctorRightMiddleGroupBox = QGroupBox("List Box")
        self.doctorRightMiddleGroupBox.setStyleSheet(style.listBoxStyleDoctor())
        self.doctorRightBottomGroupBox = QGroupBox()

        self.doctormainLeftLayout.addWidget(self.doctorsTable)
        self.doctorMainLayout.addLayout(self.doctormainLeftLayout, 70)

        self.doctorRightTopLayout.addWidget(self.doctorSearchText)
        self.doctorRightTopLayout.addWidget(self.dotorSearchEntry)
        self.doctorRightTopLayout.addWidget(self.doctorSearchBtn)
        self.doctorRightTopGroupBox.setLayout(self.doctorRightTopLayout)

        self.doctorRightMiddleLayout.addWidget(self.allDoctors)
        self.doctorRightMiddleLayout.addWidget(self.availableDoctors)
        self.doctorRightMiddleLayout.addWidget(self.notAvailableDoctors)
        self.doctorRightMiddleLayout.addWidget(self.doctorShowBtn)
        self.doctorRightMiddleGroupBox.setLayout(self.doctorRightMiddleLayout)

        self.doctormainRightLayout.addWidget(self.doctorRightTopGroupBox,20)
        self.doctormainRightLayout.addWidget(self.doctorRightMiddleGroupBox,20)
        self.doctormainRightLayout.addWidget(self.doctorRightBottomGroupBox,60)

        self.doctorMainLayout.addLayout(self.doctormainRightLayout, 30)

        self.tab2.setLayout(self.doctorMainLayout)

        #############################################################################
        self.appointmentMainLayout = QHBoxLayout()
        self.appointmentLeftLayout = QVBoxLayout()
        self.appointmentRightLayout = QHBoxLayout()

        self.appointmentRightTopGroupBox = QGroupBox("Appointments")

        self.appointmentLeftLayout.addWidget(self.appointmentTable)
        self.appointmentMainLayout.addLayout(self.appointmentLeftLayout,70)

        self.tab3.setLayout(self.appointmentMainLayout)


    def fucnNewPatient(self):
        self.newRegistration = add_patient.AddPatient()

    def funcAddDoctor(self):
        self.newDoctor = add_doctor.AddDoctor()





    def displayPatient(self):
        for i in reversed(range(self.patientTable.rowCount())):
            self.patientTable.removeRow(i)
        query = cur.execute("SELECT patient_id,registration_id,date_time,patient_name,patient_phone,patient_age,patient_sex,illness,patient_address,district,taluka,occupation,referred_by,appointment FROM patients")
        for row_data in query:
            row_number = self.patientTable.rowCount()
            self.patientTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.patientTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        self.patientTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def displayDoctors(self):
        for i in reversed(range(self.doctorsTable.rowCount())):
            self.doctorsTable.removeRow(i)

        query = cur.execute("SELECT doctor_id,doctor_name,doctor_phone,doctor_address,status FROM doctors")
        for row_data in query:
            row_number = self.doctorsTable.rowCount()
            self.doctorsTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.doctorsTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        self.doctorsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def SelectedPatient(self):
        global PatientId
        listPatient = []
        for i in range(0, 14):
            listPatient.append(self.patientTable.item(self.patientTable.currentRow(), i).text())

        # print(listPatient)
        PatientId = listPatient[0]
        self.display = DisplayPatient()
        self.display.show()

    def SelectedDoctor(self):
        global DoctorId
        listdoctors = []
        for i in range(0,5):
            listdoctors.append(self.doctorsTable.item(self.doctorsTable.currentRow(),i).text())
        DoctorId = listdoctors[0]
        self.display = DisplayDoctor()
        self.display.show()

    def SearchPatient(self):
        value = self.searchEntry.text()
        if(value==""):
            QMessageBox.information(self,"Warning","Search entry cannot be Empty")
        else:
            self.searchEntry.setText("")
            query = ("SELECT patient_id,registration_id,date_time,patient_name,patient_phone,patient_age,patient_sex,illness,patient_address,district,taluka,occupation,referred_by,appointment FROM patients WHERE registration_id LIKE ? or patient_phone LIKE ?")
            result = cur.execute(query,('%' + value + '%','%' + value + '%')).fetchall()
        if (result == []):
            QMessageBox.information(self, "Info", "No such Patient exist.")
        else:
            for i in reversed(range(self.patientTable.rowCount())):
                self.patientTable.removeRow(i)
            for row_data in result:
                row_number = self.patientTable.rowCount()
                self.patientTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.patientTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def SearchDoctor(self):
        value = self.dotorSearchEntry.text()
        if (value == ""):
            QMessageBox.information(self, "Warning", "Search entry cannot be Empty")
        else:
            self.dotorSearchEntry.setText("")
            query = ("SELECT doctor_id,doctor_name,doctor_phone,doctor_address,status FROM doctors WHERE doctor_name LIKE ? or doctor_phone LIKE ?")
            result = cur.execute(query,('%' + value + '%','%' + value + '%')).fetchall()
        if (result == []):
            QMessageBox.information(self, "Info", "No such Doctor exist.")
        else:
            for i in reversed(range(self.doctorsTable.rowCount())):
                self.doctorsTable.removeRow(i)
            for row_data in result:
                row_number = self.doctorsTable.rowCount()
                self.doctorsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.doctorsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))


    def listPatients(self):
        if(self.allpatients.isChecked()):
            self.displayPatient()
        elif(self.appointmentPatients.isChecked()):
            query = ("SELECT patient_id,registration_id,date_time,patient_name,patient_phone,patient_age,patient_sex,illness,patient_address,district,taluka,occupation,referred_by,appointment FROM patients WHERE appointment='Appointment' ")
            patients = cur.execute(query).fetchall()
            # print(patients)
            for i in reversed(range(self.patientTable.rowCount())):
                self.patientTable.removeRow(i)
            for row_data in patients:
                row_number = self.patientTable.rowCount()
                self.patientTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.patientTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        else:
            query = ("SELECT patient_id,registration_id,date_time,patient_name,patient_phone,patient_age,patient_sex,illness,patient_address,district,taluka,occupation,referred_by,appointment FROM patients WHERE appointment='Non-Appointment' ")
            patients = cur.execute(query).fetchall()
            # print(patients)
            for i in reversed(range(self.patientTable.rowCount())):
                self.patientTable.removeRow(i)
            for row_data in patients:
                row_number = self.patientTable.rowCount()
                self.patientTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.patientTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def listDoctors(self):
        if (self.allDoctors.isChecked()):
            self.displayDoctors()
        elif (self.availableDoctors.isChecked()):
            query = ("SELECT doctor_id,doctor_name,doctor_phone,doctor_address,status FROM doctors WHERE status='Available'")
            doctors = cur.execute(query).fetchall()
            # print(doctors)
            for i in reversed(range(self.doctorsTable.rowCount())):
                self.doctorsTable.removeRow(i)
            for row_data in doctors:
                row_number = self.doctorsTable.rowCount()
                self.doctorsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.doctorsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        else:
            query = (
                "SELECT doctor_id,doctor_name,doctor_phone,doctor_address,status FROM doctors WHERE status='Not Available'")
            doctors = cur.execute(query).fetchall()
            # print(doctors)
            for i in reversed(range(self.doctorsTable.rowCount())):
                self.doctorsTable.removeRow(i)
            for row_data in doctors:
                row_number = self.doctorsTable.rowCount()
                self.doctorsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.doctorsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))







class DisplayPatient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Appointment")
        self.setGeometry(350, 150, 380, 500)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon('icons/logo.png'))

        self.UI()
        self.show()

    def UI(self):
        self.patientDetails()
        self.widgets()
        self.layouts()



    def patientDetails(self):
        global PatientId
        query = ("SELECT * FROM patients WHERE patient_id=?")
        patient = cur.execute(query,(PatientId,)).fetchone()
        print(patient)
        self.patientRegId = patient[1]
        self.patientName = patient[3]
        self.patientRefer = patient[13]


    def widgets(self):
        self.titleText = QLabel("Add Appointment")
        self.titleText.setAlignment(Qt.AlignCenter)

        # self.appointmentNo = QLineEdit()
        # self.appointmentNo.setFixedWidth(30)
        self.regEntry = QLineEdit()
        self.regEntry.setFixedWidth(100)
        self.regEntry.setText(str(self.patientRegId))
        self.nameEntry = QLineEdit()
        self.nameEntry.setText(self.patientName)
        self.referEntry = QLineEdit()
        self.referEntry.setText(self.patientRefer)

        doctorQuery = ("SELECT doctor_id,doctor_name FROM doctors")
        doctors = cur.execute(doctorQuery).fetchall()
        print(doctors)
        self.doctorCombo = QComboBox()
        for doctor in doctors:
            self.doctorCombo.addItem(doctor[1],doctor[0])

        self.illness = QTextEdit()
        self.illness.setPlaceholderText("Enter illness")
        self.labReport = QComboBox()
        self.appointment = QComboBox()
        self.appointment.addItems(["Appointment","Non-Appointment"])
        self.addreportBtn = QPushButton("Add Report")
        self.appointmentBtn = QPushButton("Add Appointment")
        self.appointmentBtn.clicked.connect(self.addAppointment)
        self.updateBtn = QPushButton("Update")
        self.updateBtn.clicked.connect(self.updatePatientInfo)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        self.topLayout.addWidget(self.titleText)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Registration Id: "),self.regEntry)
        # self.bottomLayout.addRow(QLabel("Appointment No.: "),self.appointmentNo)
        self.bottomLayout.addRow(QLabel("Patient Name: "),self.nameEntry)
        self.bottomLayout.addRow(QLabel("Referred by: "),self.referEntry)
        self.bottomLayout.addRow(QLabel("Doctor Name: "),self.doctorCombo)
        self.bottomLayout.addRow(QLabel("Illness: "),self.illness)
        self.bottomLayout.addRow(QLabel("Lab & Tests: "),self.labReport)
        self.bottomLayout.addRow(QLabel("Appointment : "),self.appointment)
        self.bottomLayout.addRow(QLabel("Report: "),self.addreportBtn)
        self.bottomLayout.addRow(QLabel(""),self.appointmentBtn)
        self.bottomLayout.addRow(QLabel(""),self.updateBtn)
        self.bottomFrame.setLayout(self.bottomLayout)


        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def updatePatientInfo(self):
        global PatientId
        regId = self.regEntry.text()
        name = self.nameEntry.text()
        referredBy = self.referEntry.text()
        doctorName = self.doctorCombo.currentText()
        illness = self.illness.toPlainText()
        appointment = self.appointment.currentText()

        if(regId and name and illness !=""):
            try:
                updateQuery = ("UPDATE patients set registration_id=?,patient_name=?,referred_by=?,illness=?,appointment=? WHERE patient_id=?")
                cur.execute(updateQuery,(regId,name,referredBy,illness,appointment,PatientId))
                con.commit()
                QMessageBox.information(self, "Info", "Patient has been Updated")
            except:
                QMessageBox.information(self, "Info", "Patient has not been Updated")

        else:
            QMessageBox.information(self, "Warning", "Fields cannot be Empty")

    def addAppointment(self):
        global PatientId,dt
        regId = self.regEntry.text()
        patientName = self.nameEntry.text()
        doctorName = self.doctorCombo.currentText()
        illness = self.illness.toPlainText()
        testReport = self.labReport.currentText()
        if (regId and patientName and illness and doctorName != ""):
            try:
                appointmentQuery = ("INSERT INTO 'appointments' (registration_id,patient_name,doctor_name,test_lab,date_time) VALUES (?,?,?,?,?)")
                cur.execute(appointmentQuery, (regId,patientName,doctorName,testReport,dt))
                con.commit()
                QMessageBox.information(self, "Info", "Appointment has been added")
            except:
                QMessageBox.information(self, "Info", "Appointment has not been added")

        else:
            QMessageBox.information(self, "Warning", "Fields cannot be Empty")

##########################################################################################################
class DisplayDoctor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Doctor's Info")
        self.setGeometry(350, 150, 370, 600)
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon('icons/logo.png'))

        self.UI()
        self.show()

    def UI(self):
        self.DotorDetails()
        self.widgets()
        self.layouts()

    def DotorDetails(self):
        global DoctorId
        query = ("SELECT * FROM doctors WHERE doctor_id=?")
        doctor = cur.execute(query,(DoctorId,)).fetchone()
        print(doctor)
        self.doctorName = doctor[1]
        self.doctorPhone = doctor[2]
        self.doctorImg = doctor[3]
        self.doctorAddress = doctor[4]
        self.doctorStatus = doctor[5]

    def widgets(self):
        self.titleText = QLabel("Doctor's Info")
        self.titleText.setAlignment(Qt.AlignCenter)
        self.doctor_img = QLabel()
        self.img = QPixmap("doctor_imgs/{}".format(self.doctorImg))
        self.doctor_img.setPixmap(self.img)
        self.doctor_img.setAlignment(Qt.AlignCenter)

        self.doctorNameEntry = QLineEdit()
        self.doctorNameEntry.setText(self.doctorName)
        self.doctorPhoneEntry = QLineEdit()
        self.doctorPhoneEntry.setText(self.doctorPhone)
        self.doctorAddressEntry = QTextEdit()
        self.doctorAddressEntry.setText(self.doctorAddress)
        self.doctorStatusEntry = QComboBox()
        self.doctorStatusEntry.addItems(["Available","Not Available"])
        self.doctorStatusEntry.setCurrentText(self.doctorStatus)
        self.doctorImgBtn = QPushButton("Upload")
        self.doctorImgBtn.clicked.connect(self.uploadDoctorImg)
        self.docotrDeleteBtn = QPushButton("Delete")
        self.docotrDeleteBtn.clicked.connect(self.deleteDoctorInfo)
        self.doctorUpdateBtn = QPushButton("Update")
        self.doctorUpdateBtn.clicked.connect(self.updateDoctorInfo)
    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout= QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.doctor_img)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Doctor's Name: "),self.doctorNameEntry)
        self.bottomLayout.addRow(QLabel("Doctor's Phone: "),self.doctorPhoneEntry)
        self.bottomLayout.addRow(QLabel("Doctor's Address: "),self.doctorAddressEntry)
        self.bottomLayout.addRow(QLabel("Doctor's Status: "),self.doctorStatusEntry)
        self.bottomLayout.addRow(QLabel("Doctor's Image: "),self.doctorImgBtn)
        self.bottomLayout.addRow(QLabel(""),self.docotrDeleteBtn)
        self.bottomLayout.addRow(QLabel(""),self.doctorUpdateBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def uploadDoctorImg(self):
        size = (200, 200)
        self.filename, ok = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image files (*.jpg *.png *.jpeg)")
        if ok:
            self.doctorImg = os.path.basename(self.filename)
            Img = Image.open(self.filename)
            Img = Img.resize(size)
            Img.save("doctor_imgs/{0}".format(self.doctorImg))

    def deleteDoctorInfo(self):
        global DoctorId
        mbox = QMessageBox.question(self,"Warning","Are you want to Delete",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if (mbox == QMessageBox.Yes):
            try:
                cur.execute("DELETE FROM doctors WHERE doctor_id=?", (DoctorId))
                con.commit()
                QMessageBox.information(self, "Info", "Doctor has been deleted")
                self.close()
            except:
                QMessageBox.information(self, "Info", "Doctor has not been deleted")

    def updateDoctorInfo(self):
        global DoctorId
        Doctorname = self.doctorNameEntry.text()
        doctorPhone = self.doctorPhoneEntry.text()
        doctorAddress = self.doctorAddressEntry.toPlainText()
        doctorStatus = self.doctorStatusEntry.currentText()
        defaultImg = self.doctorImg
        if(Doctorname and doctorPhone and doctorAddress !=""):
            try:
                query = ("UPDATE doctors set doctor_name=?,doctor_phone=?,doctor_img=?,doctor_address=?,status=? WHERE doctor_id=?")
                cur.execute(query,(Doctorname,doctorPhone,defaultImg,doctorAddress,doctorStatus,DoctorId))
                con.commit()
                QMessageBox.information(self,"Info","Doctor info has been Updated")
            except:
                QMessageBox.information(self,"Info","Doctor info has not been Updated")
        else:
            QMessageBox.information(self,"Warning","Fields cannot be Empty")




def main():
    App = QApplication(sys.argv)
    win = Main()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()