from oracle import *

BRAN_ID = 1

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
        #관리할 테이블 이름
        self.tn = 'ORD'
        #버튼 텍스트 설정
        self.button1.setText("발주 추가")
        self.button2.setText("발주 삭제")
        #테이블 설정, 발주이므로 ORD
        self.table1.select(self.tn)

        #버튼 리스너 설정
        self.button1.clicked.connect(self.button1_push)
        self.button2.clicked.connect(self.button2_push)
   
    def button1_push(self):
        #추가 요청
        mb = QMessageBox(self)
        mb.setText('추가하시겠습니까?')
        mb.addButton("예", 5)
        mb.addButton("아니오", 6)
        mb.buttonClicked.connect(self.insertMethod)
        mb.show()
    def button2_push(self):
        #삭제 요청
        mb = QMessageBox(self)
        mb.setText("삭제하시겠습니까?")
        mb.addButton('예', 5)
        mb.addButton('아니오', 6)
        mb.show()
        mb.buttonClicked.connect(self.deleteMethod)


    def insertMethod(self, button):
        if button.text() == '예':
            #ORD 추가
            cursor.execute("INSERT INTO " + self.tn +" (ORD_DAT, ORD_ID, BRANCH_ID) VALUES('" 
                + str(datetime.date.today()) + "', SEQ_ORD_ID.NEXTVAL, " + str(BRAN_ID) + ")")
            cursor.execute('COMMIT')
            #리프레쉬
            self.table1.select(self.tn)
    def deleteMethod(self, button):    
        if button.text() == '예':
            #ORD 삭제
            r = self.table1.currentRow()
            cursor.execute("DELETE FROM " + self.tn
             + " WHERE (ORD_ID = " + self.table1.item(r, 1).text() + ")")
            cursor.execute('COMMIT')
        
            #refresh
            self.table1.select(self.tn)

class ORDERPROD_Dialog(basicDialog):
    def __init__(self):
        super().__init__()
        #관리할 테이블 이름
        self.tn = 'ORDERPROD'
        #버튼 텍스트 설정
        self.button1.setText("물품 추가")
        self.button2.setText("물품 삭제")
        #테이블 설정
        self.table1.select(self.tn)

        #버튼 리스너 설정
        self.button1.clicked.connect(self.button1_push)
        self.button2.clicked.connect(self.button2_push)
   
    def button1_push(self):
        #추가 요청
        mb = QMessageBox(self)
        mb.setText('추가하시겠습니까?')
        mb.addButton("예", 5)
        mb.addButton("아니오", 6)
        mb.buttonClicked.connect(self.insertMethod)
        mb.show()
    def button2_push(self):
        #삭제 요청
        mb = QMessageBox(self)
        mb.setText("삭제하시겠습니까?")
        mb.addButton('예', 5)
        mb.addButton('아니오', 6)
        mb.show()
        mb.buttonClicked.connect(self.deleteMethod)


    def insertMethod(self, button):
        #QUERY_0102 필요물품 추가
        if button.text() == '예':
            #ORD 추가
            cursor.execute("INSERT INTO " + self.tn +" (ORD_DAT, ORD_ID, BRANCH_ID) VALUES('" 
                + str(datetime.date.today()) + "', SEQ_ORD_ID.NEXTVAL, " + str(BRAN_ID) + ")")
            cursor.execute('COMMIT')
            #리프레쉬
            self.table1.select(self.tn)
            
    def deleteMethod(self, button):    
        if button.text() == '예':
            #ORD 삭제
            r = self.table1.currentRow()
            cursor.execute("DELETE FROM " + self.tn
             + " WHERE (ORD_ID = " + self.table1.item(r, 1).text() + ")")
            cursor.execute('COMMIT')
        
            #refresh
            self.table1.select(self.tn)


HOST = 'localhost'
USER = 'jja'
PASSWORD = 'ml'
cursor = access(HOST, USER, PASSWORD)
app = QApplication(sys.argv)
win = ORD_Dialog()
win.show()
app.exec_()
