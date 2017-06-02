import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import cx_Oracle as orc
import datetime

#우리 편의점 브랜치 아이디
BRAN_ID = 1

class QCustomTableWidgetItem (QTableWidgetItem):
    #실수 표현을 위해 상속켜서 관련 코드를 추가함. 
    def __init__ (self, value):
        super(QCustomTableWidgetItem, self).__init__(('%s' % value))
    def __lt__ (self, other):
        if (isinstance(other, QCustomTableWidgetItem)): 
            selfDataValue  = float(self.data(QtCore.Qt.EditRole).toString())
            otherDataValue = float(other.data(QtCore.Qt.EditRole).toString())
            return selfDataValue < otherDataValue
        else:
            return QTableWidgetItem.__lt__(self, other)
class QCustomTable(QTableWidget):
    #QTableWidget에 시퀄문과 연계시킨 메쏘드들 추가.
    def __init__(self):
        #테이블위젯과 간단한 버튼. 주로 하나의 튜플을 표시할 때!


        super().__init__()

        self.INIT_ROW = 100 #select 문 실행시 이 개수만큼 테이블을 늘려놓고 로드. 더 커지면 + INIT_ROW

        self.columnData = list #셀렉트한 결과의 칼럼 정보를 저장할 리스트.

        self.horizontalHeader().setStyleSheet("border: 3px ; border-bottom-style : double; border-color : lightgray; background : white")
        self.setColumnCount(1)
        self.setRowCount(1)
        self.setColumnWidth(0,1)
        self.setRowHeight(0,1)
    
    #테이블 배치
    def columnLoad(self):

        self.columnData =  cursor.description
        if self.columnData is not None:
            self.setColumnCount(len(self.columnData))
            lis = []
            for col in self.columnData:
                lis.append(col[0])
            self.setHorizontalHeaderLabels((lis))

        self.horizontalHeader().setSectionResizeMode(3) #컬럼의 사이즈를 텍스트 길이에 fit.
        
    
    
            
    def rowLoad(self):
        for item in  cursor:
            for c in range(0,self.columnCount()):
                self.setItem( cursor.rowcount - 1, c, QCustomTableWidgetItem(item[c]))
                #만약 셀렉트한 테이블의 튜플이 INIT_ROW 보다 많으면, 자동으로 적재할 테이블을 늘린다.
            if ( cursor.rowcount >= self.rowCount()):
                self.setRowCount(self.rowCount + self.INIT_ROW)
            #최종적으로 로드된 튜플의 개수만큼 테이블 크기를 최적화한다.
        self.setRowCount(cursor.rowcount)
        self.verticalHeader().setSectionResizeMode(3)
    #기본적인 함수지원
    def select(self, _entityName):
        #엔티티 이름을 매개변수로 받아 셀렉트 문을 실행하고 표시한다.
        try:
            cursor.execute("SELECT * FROM " + _entityName)
            self.setRowCount(self.INIT_ROW)
            self.columnLoad()
            self.rowLoad()

        except orc.DatabaseError as e : 
            mb = QMessageBox(self)
            #cx_Oracle에서 제공하는 익셉션인 e는 args 를 포함하며, 이 클래스는 message 라는 변수를 가진다.
            mb.setText("오류! : " + e.args[0].message)
            mb.show()

    def insert(self, _entityName, values):
        #키가 같을 때 등의 오류 출력하고, 오류시에는 커밋도 x.
        #필요 인풋 : 넣을 엔티티, 넣을 값들(list)
        
        #table = QCustumTable()
        #te.setC
        #te.show()
        #INSERT INTO "JJA"."EMP" (SALARY, EMPNO, EMPNAME, TEST) VALUES ('50000', '3', '제약', '2411')
        #query = "INSERT INTO " + USER + "." + self.entityList.toPlainText() + " (SALARY, EMPNO, EMPNAME, TEST) VALUES (2,4,1,2)" 
        #query = """INSERT INTO "JJA"."EMP" (SALARY, EMPNO, EMPNAME, TEST) VALUES ('50000', '3', '제약', '2411')"""
        ##
        cursor.execute(query)
       #db.commit()
    #쿼리 manipulating    
    def longQueryLoad(self, _query):
        #텍스트파일로 저장해둘 긴 쿼리를 로드후 이 메쏘드에 넣으면 결과를 표시
        #20170406_왜인지 알 수 없는 오류로 사용안하는 중. 그냥 queryLoad를 이용하겠음.
        try:
        
            err = list()
            dmlRowCount = int()
            print(_query)
            cursor.executemany(_query, err, dmlRowCount)
            self.setRowCount(self.INIT_ROW)
            self.columnLoad()
            self.rowLoad()
            #if err!=None:

        except orc.DatabaseError as e:
            mb = QMessageBox(self)
            #cx_Oracle에서 제공하는 익셉션인 e는 args 를 포함하며, 이 클래스는 message 라는 변수를 가진다.
            mb.setText("오류! : " + e.args[0])
            mb.show()

    def queryLoad(self, _query):
        #_query가 ; 로 끝나면 오류남. 미리 분리후 넣을 것.
        if ((_query != '') & (_query != '\n')):
            try:
                cursor.execute(_query)
                cursor.execute("COMMIT")
                if cursor.description != None:
                    self.setRowCount(self.INIT_ROW)
                    self.columnLoad()
                    self.rowLoad()
        
            except orc.DatabaseError as e:
                mb = QMessageBox(self)
            #cx_Oracle에서 제공하는 익셉션인 e는 args 를 포함하며, 이 클래스는 message 라는 변수를 가진다.
                mb.setText("오류! : " + e.args[0].message)
                mb.show()
    def queryLoadWithParam(self, _query, _param):
        #_query가 ; 로 끝나면 오류남. 미리 분리후 넣을 것.
        #_param은 dictionary를 이용. ex) _param = {'A':'a', 'B':'b'} 
        if ((_query != '') & (_query != '\n')):
            try:
                cursor.execute(_query, _param)
                cursor.execute("COMMIT")
                if cursor.description != None:
                    self.setRowCount(self.INIT_ROW)
                    self.columnLoad()
                    self.rowLoad()
        
            except orc.DatabaseError as e:
                mb = QMessageBox(self)
            #cx_Oracle에서 제공하는 익셉션인 e는 args 를 포함하며, 이 클래스는 message 라는 변수를 가진다.
                mb.setText("오류! : " + e.args[0].message)
                mb.show()
    #file i/o. 읽은 쿼리들을 반환한다.
    def fileRead(self, _fileName):
        try:
            
            f = open(_fileName, 'r')
            querys = f.read()
            querys = querys.split(';')

            return querys

        except FileNotFoundError as e:
            mb = QMessageBox(self)
            #
            mb.setText("오류! : " + e.strerror)
            mb.show()
    def setCursor(self, _cursor):
        self.cursor = _cursor   ###딥 카피를 해야할 것 같은데...? 굳이?




class Entity_Manip(QDialog):
    def __init__(self):
        #엔티티의 디그리, 카디널리티를 읽어와서 기본 틀을 만든다.
        #알아낼 필요없이 Qt 에서 제공하는 시퀄 인터페이스를 이용해보자. ___Fail
        super().__init__()
        QWidget.setStyleSheet(self, """font: large "윤고딕340";""")
        self.setGeometry(100,100, 1142, 500)
        self.INIT_ROW = 100
        self.l1 = QVBoxLayout(self)
        self.l2 = QHBoxLayout()
        self.entityList = QTextEdit("query/query_test.txt") #나중에 리스트박스로 바꾸자.
        self.entityList.setWordWrapMode(True)
        self.entityList.setFixedHeight(35)
        
        self.selectable1t = QPushButton("SELECT", self)
        self.selectable1t.clicked.connect(self.select)
        self.insertable1t = QPushButton("ADD", self)
        #self.insertable1t.clicked.connect(self.insert)
        self.executeQueryBt = QPushButton("EXECUTE", self)
        self.executeQueryBt.clicked.connect(self.execute)
        self.fileBt = QPushButton("FILE_QUERY", self)
        self.fileBt.clicked.connect(self.fileRead)

        self.l2.addWidget(self.entityList)
        self.l2.addWidget(self.selectable1t)
        self.l2.addWidget(self.insertable1t)
        self.l2.addWidget(self.executeQueryBt)
        self.l2.addWidget(self.fileBt)
        self.l1.addLayout(self.l2)
        self.col = int  #select 한 테이블의 column 개수
        self.row = int  #select 한 테이블의 row 개수. (select한 튜플 개수만.)
        self.table1 = QCustomTable()
        #self.table1.setCursor(cursor)

        self.l1.addWidget(self.table1)
    def select(self):
        self.table1.select(self.entityList.toPlainText())
    def execute(self):
        self.table1.queryLoad(self.entityList.toPlainText())
    def fileRead(self):
        qs = self.table1.fileRead(self.entityList.toPlainText())
        for q in qs:
            if q != '':
                self.table1.queryLoad(q)
    def fileReadWithParam(self, _param):
        qs = self.table1.fileRead(self.entityList.toPlainText())
        for q in qs:
            if q != '':
                self.table1.queryLoadWithParam(q,_param)    

#테이블을 띄우는 리스트 1개
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
        

#query1
class qrdialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100, 1142, 500)

        self.l1 = QGridLayout(self)
        od = datetime.date(2017,5,24)
        dd = datetime.date(2017,6,1)
        self.param = {'ORD_DAT':od, 'ORD_ID':'1', 'PROD_ID':'2', 'ORD_REQUEST_QUANTITY':'3', 'DEPOSIT_DAT':dd}
        self.pList = {1:'ORD_DAT',2:'ORD_ID', 3:'PROD_ID',4:'ORD_REQUEST_QUANTITY', 5:'DEPOSIT_DAT'}
        
        self.table1 = QCustomTable()
        #self.table1.hide()
        self.table1.setCursor(cursor)
        
        self.label1 = QLabel("QUERY ROUTE")
        self.label2 = QLabel(self.pList[3])
        self.label3 = QLabel(self.pList[4])
        self.label4 = QLabel(self.pList[5])

        self.tb1 = QTextEdit()
        self.tb1.setText('query/query_0102.txt')
        self.tb1.setFixedHeight(35)
        self.tb2 = QTextEdit()
        self.tb2.setText(str(self.param[self.pList[3]]))
        self.tb2.setFixedHeight(35)
        self.tb3 = QTextEdit()
        self.tb3.setText(str(self.param[self.pList[4]]))
        self.tb3.setFixedHeight(35)
        self.tb4 = QTextEdit()
        self.tb4.setText(str(self.param[self.pList[5]]))
        self.tb4.setFixedHeight(35)

        self.OkBt = QPushButton("Execute")
        self.OkBt.clicked.connect(self.execute)
        self.CancelBt = QPushButton("Show")
        self.CancelBt.clicked.connect(self.exe1)

        self.l1.addWidget(self.label1, 0, 0)
        self.l1.addWidget(self.tb1, 0, 1)
        self.l1.addWidget(self.label2)
        self.l1.addWidget(self.tb2)
        self.l1.addWidget(self.label3)
        self.l1.addWidget(self.tb3)
        self.l1.addWidget(self.label4)
        self.l1.addWidget(self.tb4)
        self.l1.addWidget(self.OkBt)
        self.l1.addWidget(self.CancelBt)
        
    def execute(self):

        qs = self.table1.fileRead(self.tb1.toPlainText())
        self.param[self.pList[3]] = self.tb2.toPlainText()
        self.param[self.pList[4]] = self.tb3.toPlainText()
        self.param[self.pList[5]] = self.tb4.toPlainText()
        for q in qs:
            self.table1.queryLoadWithParam(q, self.param)

        
    def exe1(self):
        #self.table1.show()
        #self.hide()
        qs = self.table1.fileRead(self.tb1.toPlainText())
        for q in qs:
            self.table1.queryLoad(q)
#query
class qdialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setGeometry(100,100, 1142, 500)
        self.l0 = QVBoxLayout(self)
        self.l1 = QGridLayout()

        #쿼리와 연동할 매개변수를 저장하는 딕셔너리
        self.param = dict()
        #쿼리를 파싱해서 필요 매개변수 이름을 저장할 리스트
        self.pList = list()
        
        self.lbList =list()
        self.tbList = list()
        #GUI로 띄울 테이블
        self.paramTable = QTableWidget()
        self.table1 = QCustomTable()
        #self.table1.hide()
        self.table1.setCursor(cursor)
        
        self.label1 = QLabel("QUERY ROUTE")


        self.tb1 = QTextEdit()
        self.tb1.setText('query/query_0102.txt')
        self.tb1.setFixedHeight(35)
        self.parseBt = QPushButton("Parse")
        self.parseBt.clicked.connect(self.parse)

        self.OkBt = QPushButton("Execute")
        self.OkBt.clicked.connect(self.execute)
        self.CancelBt = QPushButton("Show")
        self.CancelBt.clicked.connect(self.exe1)

        self.l1.addWidget(self.label1, 0, 0)
        self.l1.addWidget(self.tb1, 0, 1)
        self.l1.addWidget(self.parseBt, 0,3)
        self.l0.addLayout(self.l1)
        
    #매개변수를 포함하는 쿼리에 대한 execute    
    def execute(self):
        if len(self.pList) != 0:
            for n in range(len(self.pList)):
                if self.paramTable.item(0,n) != 0:
                    self.param[self.pList[n]] = self.paramTable.item(0,n).text()
                else:
                    print(n + "번째 파라미터가 비었습니다.")
            self.table1.queryLoadWithParam(self.qtag, self.param)
    #쿼리에서 요구하는 매개변수 리스트를 파싱함.
    def parse(self):
        q = self.table1.fileRead(self.tb1.toPlainText())
        
        self.qtag = cursor.prepare(q[0])
        #쿼리에서 요구하는 매개변수를 pList에 저장
        self.pList = cursor.bindnames()
        #GUI화 : 레이블과 텍스트상자 만들기
        for n in range(len(self.pList)):
            self.lbList.append(QLabel(self.pList[n]))
            self.tbList.append(QTextEdit())
            self.lbList[n].setFixedHeight(35)
            self.tbList[n].setFixedHeight(35)

        self.l1.addWidget(self.OkBt, 2, 2)
        self.l1.addWidget(self.CancelBt, 2, 3)
        self.paramTable.setColumnCount(len(self.pList))
        self.paramTable.setRowCount(1)
        self.paramTable.setMaximumHeight(80)
        self.paramTable.setHorizontalHeaderLabels(self.pList)
        self.l1.addWidget(self.paramTable, 1,0,1,-1)
        self.l0.addWidget(self.table1)
        
    #매개변수를 따지지 않고 쿼리 execute
    def exe1(self):
        #self.table1.show()
        #self.hide()
        qs = self.table1.fileRead(self.tb1.toPlainText())
        for q in qs:
            self.table1.queryLoad(q)


#로그인 다이얼로그

#로그인 다이얼로그
class loginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.l1 = QGridLayout(self)

        self.label1 = QLabel("HOST NAME")
        self.label2 = QLabel("DBNAME")
        self.label3 = QLabel("USER")
        self.label4 = QLabel("PASSWORD")

        self.tb1 = QTextEdit()
        self.tb1.setText(HOST)
        self.tb1.setFixedHeight(35)
        self.tb2 = QTextEdit()
        self.tb2.setText(DBNAME)
        self.tb2.setFixedHeight(35)
        self.tb3 = QTextEdit()
        self.tb3.setText(USER)
        self.tb3.setFixedHeight(35)
        self.tb4 = QTextEdit()
        self.tb4.setText(PASSWORD)
        self.tb4.setFixedHeight(35)

        self.OkBt = QPushButton("Access")
        self.OkBt.clicked.connect(self.access)
        self.CancelBt = QPushButton("Cancel")
        self.CancelBt.clicked.connect(self.hide)

        self.l1.addWidget(self.label1, 0, 0)
        self.l1.addWidget(self.tb1, 0, 1)
        self.l1.addWidget(self.label2)
        self.l1.addWidget(self.tb2)
        self.l1.addWidget(self.label3)
        self.l1.addWidget(self.tb3)
        self.l1.addWidget(self.label4)
        self.l1.addWidget(self.tb4)
        self.l1.addWidget(self.OkBt)
        self.l1.addWidget(self.CancelBt)

    def access(self):
        #self.dsn = orc.makedsn("52.79.194.219", 1521, "XE")  #호스트이름, 포트번호, SID
        self.dsn = orc.makedsn("localhost", 1521, "XE")
        self.db = orc.connect("jja", "ml", self.dsn)
        #커서 변수를 전역변수로 설정했는데, 이게 비효율적일 수 있을 것 같다.
        #나중에 다르게 바꾸던가, 메인 윈도우 하나를 선정해서 그 클래스의 변수로 활용해야 할듯.
        #그러려면 그 메인 윈도우 클래스의 변수에 접근할 수 있도록 해야한다..
        global cursor 
        cursor = self.db.cursor()
        #self.window = Entity_Manip()
        self.hide()
        #self.window.show()
        self.q1 = ORD_Dialog()
        self.q1.show()




HOST = "52.79.194.219"
USER = "team"
PASSWORD = "team"
DBNAME = "db"


app = QApplication(sys.argv)
win = loginWindow()
win.show()
app.exec_()
