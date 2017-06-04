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

def access():
    dsn = makedsn(HOST, 1521, 'XE')
    db = connect(USER, PASSWORD, dsn)
    global cursor
    cursor = db.cursor()
    

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
                lis.append(col[0])
            self.setHorizontalHeaderLabels((lis))
        #컬럼의 사이즈를 텍스트 길이에 fit.
        self.horizontalHeader().setSectionResizeMode(3) 
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
                cursor.execute("COMMIT")
                if cursor.description != None:
                    self.setRowCount(self.INIT_ROW)
                    self.columnLoad()
                    self.rowLoad()
        
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
                cursor.execute("COMMIT")
                if cursor.description != None:
                    self.setRowCount(self.INIT_ROW)
                    self.columnLoad()
                    self.rowLoad()
        
            except DatabaseError as e:
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
