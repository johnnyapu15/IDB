#20170604_JJA

#cx_Oracle을 이용하기 편한 몇개의 클래스로 정리.
#접속 정보와 access 메소드를 가지고 있음.
#메인화면에서 이 access 메소드를 실행해 줄 것.

#class QCustomTable : db 테이블을 표시할 때 편리하도록 만든 테이블 위젯

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *

from cx_Oracle import *
import datetime


#
HOST = "52.79.194.219"
USER = 'team'
PASSWORD = 'team'
DBNAME = 'db'

COLUMN_DIC ={'PUB_DEP_ID':'공공요금 수납 ID',
'BRANCH_ID':'지점 ID',
'END_TIME':'끝시간',
'START_DAT':'시작 날짜',
'START_TIME':'시작 시간',
'EMP_ID':'직원 ID',
'TIME_DUR':'시간 간격',
'BUY_PRICE':'구매단가',
'MAIN_CATEGORY_CODE':'대분류 코드',
'PROD_NAME':'물품명',
'PROD_ID':'물품 ID',
'SUB_CATEGORY_CODE':'소분류 코드',
'CUSTOMER_COST':'소비자가',
'UOS25_EXCLUSIVE':'우리편의점 전용물품',
'DISTRIB_PERIOD':'유통기간',
'SELL_PRICE':'판매단가',
'PROD_ID':'물품 ID',
'PROD_NAME':'물품명',
'RETURN_DAT':'반품 날짜',
'RETURN_CAUSE_CODE':'반품 사유 코드',
'RETURN_REQUEST_QUANTITY':'반품 의뢰 수량',
'RETURN_PROCESS_RESULT':'반품 처리 결과',
'RETURN_ID':'반품 ID',
'LOTT_ID':'복권 ID',
'BRANCH_ID':'지점 ID',
'CONTACT':'연락처',
'ADDRESS':'주소',
'AGE':'나이',
'MILEAGE':'마일리지',
'GENDER_CODE':'성별 코드',
'CUSTOMER_ID':'소비자 ID',
'NAME':'이름',
'PROD_ID':'물품 ID',
'PROD_NAME':'물품명',
'LOSS_CAUSE_CODE':'손실 원인 코드',
'QUANTITY':'수량',
'INVEST_DAT':'파악 날짜',
'INVEST_NO':'파악 회차',
'COM_NAME':'업체명',
'COM_ID':'업체 ID',
'CONTACT':'연락처',
'ADDRESS':'주소',
'EVENT_NAME':'이벤트명',
'EVENT_START_DAT':'이벤트시작날짜',
'EVENT_END_DAT':'이벤트종료날짜',
'EVENT_ID':'이벤트 ID',
'DISCOUNT_UNIT':'할인단위',
'DISCOUNT_RATIO':'할인율',
'PROD_ID':'물품 ID',
'PROD_NAME':'물품명',
'EVENT_ID':'이벤트 ID',
'BRANCH_ID':'지점 ID',
'FRANCHISE_FEE':'가맹비',
'DAT':'날짜',
'SALE':'매출',
'PROFIT_COST':'수익금',
'NET_PROFIT':'순이익',
'PRICE':'원가',
'UPKEEP_COST':'유지비',
'PAYROLL_COST':'인건비',
'BRANCH_ID':'지점 ID',
'ORD_DAT':'발주 날짜',
'ORD_COST':'발주액',
'ORD_ID':'주문 ID',
'CONTACT':'연락처',
'ADDRESS':'주소',
'BRANCH_MANAGER':'지점장',
'BRANCH_ID':'지점 ID',
'SELL_MARGIN_RATIO':'판매마진지불비율',
'SALARY':'급여',
'SALARY_CODE':'급여 코드',
'BRANCH_ID':'지점 ID',
'EMP_GRADE_CODE':'직원 등급 코드',
'CONTACT':'연락처',
'NAME':'이름',
'EMP_ID':'직원 ID',
'PROD_ID':'물품 ID',
'PROD_NAME':'물품명',
'EXPIRATION_DAT':'유통 기한',
'MANUFACTURE_DAT':'제조 날짜',
'DISPLAY_QUANTITY':'진열 수량',
'EVENT_FLAG':'행사 유무',
'PROD_ID':'물품 ID',
'PROD_NAME':'물품명',
'QUANTITY':'수량',
'EXPIRATION_DAT':'유통기한',
'MANUFACTURE_DAT':'제조날짜',
'BRANCH_ID':'지점 ID',
'DELIV_ID':'택배 ID',
'CUSTOMER_ID':'소비자 ID',
'SELL_DAT':'판매 날짜',
'SELL_TIME':'판매 시간',
'SELL_ID':'판매 ID',
'SELL_COST':'판매액',
'PROD_ID':'물품 ID',
'PROD_NAME':'물품명',
'QUANTITY':'수량',
'SELL_ID':'판매 ID',
'SELL_COST':'판매액',
'PROD_ID':'물품 ID',
'PROD_NAME':'물품명',
'QUANTITY':'수량',
'DISPOSE_PROCESS_DAT':'폐기 처리 날짜',
'PROD_ID':'물품 ID',
'PROD_NAME':'물품명',
'ORD_REQUEST_QUANTITY':'발주 의뢰 수량',
'ORD_RESULT_QUANTITY':'발주 결과 수량',
'DEPOSIT_RESULT_QUANTITY':'수령 결과 수량',
'DEPOSIT_DAT':'수령 날짜',
'ATM_ID':'ATM ID',
'BRANCH_ID':'지점 ID'}

def access(hst, usr, pw):
    dsn = makedsn(hst, 1521, 'XE')
    db = connect(usr, pw, dsn)
    global cursor
    cursor = db.cursor()
    return cursor
    

class QCustomTableWidgetItem(QTableWidgetItem):
    def __init__(self, value):
        super(QCustomTableWidgetItem, self).__init__(('%s' % value))
    def __lt__(self, other):
        if (isinstance(other, QCustomTableWidgetItem)):
            selfDataValue  = float(self.data(QtCore.Qt.EditRole).toString())
            otherDataValue = float(other.data(QtCore.Qt.EditRole).toString())
            return selfDataValue < otherDataValue
        else:
            return QTableWidgetItem.__lt__(self, other)

class QCustomTable(QTableWidget):
    def __init__(self):
        
        super().__init__()

        self.INIT_ROW = 100

        self.columnData = list
        self.tableName = ''
        self.horizontalHeader().setStyleSheet("border: 3px ; border-bottom-style : double; border-color : lightgray; background : white")
        self.setColumnCount(1)
        self.setRowCount(1)
        self.setColumnWidth(0,1)
        self.setRowHeight(0,1)

        #테이블 배치
    def columnLoad(self):
        self.columnData = cursor.description
        if self.columnData is not None:
            self.setColumnCount(len(self.columnData))
            lis = []
            for col in self.columnData:
                lis.append(COLUMN_DIC[col[0]])
            self.setHorizontalHeaderLabels((lis))
        #컬럼의 사이즈를 텍스트 길이에 fit.
        # self.horizontalHeader().setSectionResizeMode(3)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        self.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeToContents) 
        self.horizontalHeader().setSectionResizeMode(1,QHeaderView.ResizeToContents) 
#        self.horizontalHeader().setSectionResizeMode(4,QHeaderView.ResizeToContents) 
#        self.horizontalHeader().setSectionResizeMode(6,QHeaderView.ResizeToContents)  
    def rowLoad(self):
        for item in cursor:
            for c in range(0,self.columnCount()):
                text = str(item[c])
                #만약 타입이 시간일 경우 10자리로 끊는다.
                if str(cursor.description[c][1]) == "<class 'cx_Oracle.DATETIME'>":
                    text = (str(text))[0:10]
                if str(cursor.description[c][1]) == "<class 'cx_Oracle.TIMESTAMP'>":
                    text = (str(text))[0:19]
                self.setItem( cursor.rowcount - 1, c, QCustomTableWidgetItem(text))
                self.item( cursor.rowcount - 1, c).setTextAlignment(Qt.AlignHCenter)
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
            self.tableName = _entityName
            cursor.execute("SELECT * FROM " + _entityName)
            self.setRowCount(self.INIT_ROW)
            self.columnLoad()
            self.rowLoad()

        except DatabaseError as e : 
            mb = QMessageBox(self)
            #cx_Oracle에서 제공하는 익셉션인 e는 args 를 포함하며, 이 클래스는 message 라는 변수를 가진다.
            mb.setText("오류! : " + e.args[0].message)
            mb.show()   
    def execute(self, _query):
        #여기서 접근가능한 커서로 쿼리를 실행한다.
        try:
            cursor.execute(_query)
            if cursor.description != None:
                self.setRowCount(self.INIT_ROW)
                self.columnLoad()
                self.rowLoad()
            cursor.execute("COMMIT")
        except DatabaseError as e : 
            mb = QMessageBox(self)
            #cx_Oracle에서 제공하는 익셉션인 e는 args 를 포함하며, 이 클래스는 message 라는 변수를 가진다.
            mb.setText("오류! : " + e.args[0].message)
            mb.show()     
    #테이블 이름으로 검색해서 컬럼값만 지정해줌
    def columnSet(self, _entityName, _row):
        try:
            cursor.execute("SELECT * FROM " + _entityName)
            self.columnLoad()
            self.setRowCount(1)
            if _row > 0:
                self.setRowCount(_row)
            self.verticalHeader().setSectionResizeMode(3)

        except DatabaseError as e : 
            mb = QMessageBox(self)
            #cx_Oracle에서 제공하는 익셉션인 e는 args 를 포함하며, 이 클래스는 message 라는 변수를 가진다.
            mb.setText("오류! : " + e.args[0].message)
            mb.show() 
    #매개변수없는 쿼리 실행    
    def queryLoad(self, _query):
        #_query가 ; 로 끝나면 오류남. 미리 분리후 넣을 것.
        if ((_query != '') & (_query != '\n')):
            try:
                cursor.execute(_query)
                if cursor.description != None:
                    self.setRowCount(self.INIT_ROW)
                    self.columnLoad()
                    self.rowLoad()
                cursor.execute("COMMIT")
            except DatabaseError as e:
                mb = QMessageBox(self)
            #cx_Oracle에서 제공하는 익셉션인 e는 args 를 포함하며, 이 클래스는 message 라는 변수를 가진다.
                mb.setText("오류! : " + e.args[0].message)
                mb.show()
    #매개변수를 가지는 쿼리 실행
    def queryLoadWithParam(self, _query, _param):
        #_query가 ; 로 끝나면 오류남. 미리 분리후 넣을 것.
        #_param은 dictionary를 이용. ex) _param = {'A':'a', 'B':'b'} 
        if ((_query != '') & (_query != '\n')):
            try:
                cursor.execute(_query, _param)
                if cursor.description != None:
                    self.setRowCount(self.INIT_ROW)
                    self.columnLoad()
                    self.rowLoad()
                cursor.execute("COMMIT")
            except DatabaseError as e:
                mb = QMessageBox(self)
            #cx_Oracle에서 제공하는 익셉션인 e는 args 를 포함하며, 이 클래스는 message 라는 변수를 가진다.
                mb.setText("오류! : " + e.args[0].message)
                mb.show()
    #file i/o. 읽은 쿼리들을 반환한다.
    def fileRead(self, _fileName):
        try:
            
            f = open('query/'+_fileName, 'r')
            querys = f.read()
            querys = querys.split(';')

            return querys

        except FileNotFoundError as e:
            mb = QMessageBox(self)
            #
            mb.setText("오류! : " + e.strerror)
            mb.show()

    
    def fileExecute(self, _fileName, _param):
        qs = self.fileRead(_fileName)
        for q in qs:
            self.queryLoadWithParam(q, _param)


    def refresh(self):
        self.select(self.tableName)