from oracle import *

#테이블을 띄우는 리스트 1개,
#ADD, DEL 버튼 2개 로 이루어진 다이얼로그
class basicDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1500, 600)
        
        self.l0 = QGridLayout(self)
        self.listBox1 = QListWidget()
        self.table1 = QCustomTable()
        self.button1 = QPushButton()
        self.button2 = QPushButton()

        self.listBox1.setFixedSize(self.width()/4, self.height())
        self.table1.setFixedHeight(self.height())
        self.button1.setFixedHeight(self.height()/2)
        self.button2.setFixedHeight(self.height()/2)
        self.button1.setFixedSize(self.width()/4, self.height()/2)

        self.l0.addWidget(self.listBox1, 0, 0, -1,1)
        self.l0.addWidget(self.table1, 0,1, -1,1)
        self.l0.addWidget(self.button1, 0,2)
        self.l0.addWidget(self.button2, 1,2)

    #    self.button1.clicked.connect(self.button1_push)
    

class ORD_Dialog(basicDialog):
    def __init__(self):
        super().__init__()
        #버튼 텍스트 설정
        self.button1.setText("발주 추가")
        self.button2.setText("발주 삭제")
        #테이블 설정, 발주이므로 ORD
        self.table1.select("ORD")

        #버튼 리스너 설정
        self.button1.clicked.connect(self.button1_push)
        self.button2.clicked.connect(self.button2_push)
   
    def button1_push(self):
        #ORD 추가
        cursor.execute("INSERT INTO ORD (ORD_DAT, ORD_ID, BRANCH_ID) VALUES('" 
            + str(datetime.date.today()) + "', SEQ_ORD_ID.NEXTVAL, " + str(BRAN_ID) + ")")
        cursor.execute('COMMIT')
        #리프레쉬
        self.table1.select("ORD")
        
    def button2_push(self):
        print("삭제버튼이 눌려져버렸당ㅠㅠ")
        

access()
app = QApplication(sys.argv)
win = ORD_Dialog()
win.show()
app.exec_()
