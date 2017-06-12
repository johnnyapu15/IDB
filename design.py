import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from oracle import *



class MyWindow(QMainWindow, uic.loadUiType("test1.ui")[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.t1 = QCustomTable()
        self.gridLayout.addWidget(self.t1)
        self.t1.columnSet("ORD",1)
        #self.form_class.tableWidget_2.clicked.coonect(self.btn_clicked)
        self.pushButton.clicked.connect(self.btn_clicked)   
        # self.lineEdit_3.textChanged.connect(self.lineEditChanged)
    def www(self):
        print('testtest')
    def btn_clicked(self):
        self.w2 = MyWindow()
        #self.hide()
        self.w2.show()
    # def lineEditChanged(self):
    #     self.lineEdit_8.setText("새우깡")

if __name__ == "__main__":
    global cursor
    cursor = access('localhost', 'jja', 'ml')
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    