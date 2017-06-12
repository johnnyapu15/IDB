import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from oracle import *
import jjap

form_class = uic.loadUiType("ui/1.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        ###
        super().__init__()
        self.setupUi(self)
        self.t1 = QCustomTable()    #EMP
        self.t2 = QCustomTable()    #PROD
        self.t3 = QCustomTable()    #필요물품
        self.t4 = QCustomTable()    #WAREPROD
        self.t5 = QCustomTable()    #반품물품
        self.t6 = QCustomTable()    #DISPROD
        self.t7 = QCustomTable()    #EVENT
        self.t8 = QCustomTable()    #ORD
        self.gridLayout.addWidget(self.t1)
        self.t1.select("EMP")
        
        # self.gridLayout_3.addWidget(self.t3)    #필요물품
        # self.t3.select("")
        
        self.gridLayout_5.addWidget(self.t5)    #반품물품
        self.t5.select("RPROD")

        self.gridLayout_2.addWidget(self.t2)    
        self.t2.select("PROD")
        
        # self.gridLayout_6.addWidget(self.t4)
        # self.t4.select("WAREPROD")

        self.gridLayout_8.addWidget(self.t8)
        self.t8.select("ORD")

        self.gridLayout_11.addWidget(self.t7)
        self.t7.select("EVENT")

        ###################정주안 작업####################

        #####발주 관련##########

        self.pushButton_27.clicked.connect(self.ins_ORD)   #발주 추가
        self.pushButton_28.clicked.connect(self.del_ORD)   #발주 삭제
        self.t8.doubleClicked.connect(self.call_ORDPROD)   #필요물품 추가
        self.pushButton_8.clicked.connect(self.dep_ORD)
        self.pushButton_19.clicked.connect(self.exe_ORD)    #발주하기
        self.pushButton_34.clicked.connect(self.search_ORD) #날짜 검색
        self.dateEdit.setDate(datetime.date.today())
        self.dateEdit_5.setDate(datetime.date.today())
        ########################

        #####반품 관련###########
        
        #반품 생성 버튼
        self.pushButton_24.clicked.connect(self.ins_RTN)

        #반품 버튼
        self.pushButton_26.clicked.connect(self.exe_RTN)

        ########################

        #################################################

        self.pushButton_42.clicked.connect(self.call_DPROD)     #폐기물품
        self.pushButton_35.clicked.connect(self.call_LPROD)     #재고파악

        self.lineEdit.editingFinished.connect(self.set0)
        self.comboBox.currentIndexChanged.connect(self.selected_widget)
        self.stackedWidget.setCurrentIndex(0) #첫화면 띄우도록
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

    def set0(self): #위젯을 판매 페이지로
        self.stackedWidget.setCurrentIndex(0)   
        self.comboBox.setCurrentIndex(0)
    def selected_widget(self):
        self.stackedWidget.setCurrentIndex(self.comboBox.currentIndex())
    
    ######발주관련################
    def call_ORDPROD(self):
        self.w1 = ORD_PROD()
        self.w1.find_id(self.t8.item(self.t8.currentRow(), 1).text())
        self.w1.show()          
    def ins_ORD(self):
        jjap.bt1(self, self.t8, 'query_0101.txt', {'ORD_DAT':str(datetime.date.today()), 'BRANCH_ID':'1000'})
    def del_ORD(self):
        jjap.bt2(self, self.t8, 'query_0401.txt', {'ORD_ID':self.t8.item(self.t8.currentRow(), 1).text()})
    #발주 정상수령 버튼
    def dep_ORD(self):
        w1 = ORD_PROD()
        w1.find_id(self.t8.item(self.t8.currentRow(), 1).text())
        
        for i in range(w1.t1.rowCount()):
            if w1.t1.item(i,4).text() == 'None':
                dic = {'ORD_ID':w1.t1.item(i,2).text(),'PROD_ID':w1.t1.item(i,0).text(),
                'ORD_RESULT_QUANTITY':w1.t1.item(i,3).text(),'DEPOSIT_DAT':str(datetime.date.today()), 'MANUFACTURE_DAT':str(datetime.date.today())}

                w1.t1.fileExecute('query_0301.txt', 
                {'ORD_ID':dic['ORD_ID'], 'PROD_ID':dic['PROD_ID'], 'ORD_RESULT_QUANTITY':dic['ORD_RESULT_QUANTITY']
                , 'DEPOSIT_DAT':dic['DEPOSIT_DAT']})
                tmpt = QCustomTable()

                tmpt.fileExecute('query_0302.txt',{'PROD_ID':dic['PROD_ID'],'MANUFACTURE_DAT':dic['MANUFACTURE_DAT']})
                if tmpt.rowCount() == 0:
                    #없을 경우 새로 생성
                    tmpt.fileExecute('query_0304.txt', 
                    {'QUANTITY':dic['ORD_RESULT_QUANTITY'], 'MANUFACTURE_DAT':dic['MANUFACTURE_DAT'],
                    'PROD_ID':dic['PROD_ID']})
                else:
                    #있을 경우 추가
                    tmpt.fileExecute('query_0303.txt', 
                    {'QUANTITY':dic['ORD_RESULT_QUANTITY'], 'MANUFACTURE_DAT':dic['MANUFACTURE_DAT'],
                    'PROD_ID':dic['PROD_ID']})
        mb = QMessageBox(self,text = '정상수령 처리되었습니다.')
        mb.show()
    def exe_ORD(self):
        mb = QMessageBox(self, text = self.t8.item(self.t8.currentRow(),1).text() + '번 주문이 발주되었습니다.')
        mb.show()
    #날짜로 검색
    def search_ORD(self):
        self.t8.fileExecute('query_0204.txt',{'START_DAY':self.dateEdit.text(), 'END_DAY':self.dateEdit_5.text()})
        
    #############################

    #####반품관련#################
    #반품 생성 버튼
    def ins_RTN(self):
        self.w1 = RPROD(self)
        self.w1.show()

    #반품 버튼
    def exe_RTN(self):
        mb = QMessageBox(self, text = self.t5.item(self.t5.currentRow(),6).text() + '가(이) 반품처리되었습니다.')
        mb.show()
    #############################
    
    
    def call_DPROD(self):
        self.w1 = D_PROD()
        self.w1.show()      
    def call_LPROD(self):
        self.w1 = L_PROD()
        self.w1.show() 

    

    #버튼이 클릭되었을 때 해당 테이블을 리프레쉬합니다.
    def msgClicked(self, table):
        table.refresh()

class ORD_PROD(QDialog,uic.loadUiType("ui/필요물품.ui")[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.t1 = QCustomTable()
        self.t1.select('ORDPROD')
        self.gridLayout_10.addWidget(self.t1)
        self.ord_id = 0
        #필요물품 추가
        self.pushButton_27.clicked.connect(self.call_ORDPROD_FIND)
        #필요물품 삭제(테이블에서 아이템 선택하고 있어야함)
        self.pushButton_28.clicked.connect(self.del_ORDPROD)
        #완료버튼. 종료와 동일
        self.pushButton_29.clicked.connect(self.hide)
        #수령확인
        #각 물품들을 테이블에서 수정할만큼 한 후 버튼을 누르면 수정 쿼리 실행
        #단 수령갯수와 수령날짜로 한정짓는다.
        self.pushButton_8.clicked.connect(self.deposit)
    def find_id(self, ord_id):
        if ord_id != '':
            self.ord_id = int(ord_id)
        self.t1.execute("select * from ordprod where ORD_ID = " + str(self.ord_id))
        self.groupBox.setTitle("ORD_ID : " + str(self.ord_id) + " - 필요물품 목록")
    def call_ORDPROD_FIND(self):
        self.w1 = ORDPROD_FIND(self)
        self.w1.ord_id = self.ord_id
        self.w1.show()
    def del_ORDPROD(self):
        jjap.bt2(self, self.t1, 'query_0402.txt', {'ORD_ID':self.ord_id, 'PROD_ID':self.t1.item(self.t1.currentRow(), 0).text()})
    def msgClicked(self, table):
        self.find_id('')
    def deposit(self):
        #수령확인
        for i in range(self.t1.rowCount()):
            if self.t1.item(i,4).text() != 'None':
                dic = {'ORD_ID':self.t1.item(i,2).text(),'PROD_ID':self.t1.item(i,0).text(),
                'ORD_RESULT_QUANTITY':self.t1.item(i,4).text(), 'DEPOSIT_DAT':self.t1.item(i,5).text(), 'MANUFACTURE_DAT':str(datetime.date.today())}
                if dic['DEPOSIT_DAT'] == 'None':
                    dic['DEPOSIT_DAT'] = str(datetime.date.today())
                self.t1.fileExecute('query_0301.txt', 
                {'ORD_ID':dic['ORD_ID'], 'PROD_ID':dic['PROD_ID'], 'ORD_RESULT_QUANTITY':dic['ORD_RESULT_QUANTITY']
                , 'DEPOSIT_DAT':dic['DEPOSIT_DAT']})
                tmpt = QCustomTable()

                tmpt.fileExecute('query_0302.txt',{'PROD_ID':dic['PROD_ID'],'MANUFACTURE_DAT':dic['MANUFACTURE_DAT']})
                if tmpt.rowCount() == 0:
                    #없을 경우 새로 생성
                    tmpt.fileExecute('query_0304.txt', 
                    {'QUANTITY':dic['ORD_RESULT_QUANTITY'], 'MANUFACTURE_DAT':dic['MANUFACTURE_DAT'],
                    'PROD_ID':dic['PROD_ID']})
                else:
                    #있을 경우 추가
                    tmpt.fileExecute('query_0303.txt', 
                    {'QUANTITY':dic['ORD_RESULT_QUANTITY'], 'MANUFACTURE_DAT':dic['MANUFACTURE_DAT'],
                    'PROD_ID':dic['PROD_ID']})
                mb = QMessageBox(self,text = "창고물품에 추가하였습니다.")
                mb.show()
                
        self.find_id('')

class ORDPROD_FIND(QDialog,uic.loadUiType("ui/필요물품검색.ui")[0]):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.t1 = QCustomTable()
        self.gridLayout_11.addWidget(self.t1)
        self.t1.select('PROD')
        self.ord_id = 0
        #검색버튼
        self.pushButton_6.clicked.connect(self.search)
        #테이블 아이템 더블클릭 -> 해당 아이템 정보를 전달해야함
        self.t1.doubleClicked.connect(self.addItem)
        #완료버튼
        self.pushButton_2.clicked.connect(self.addItem)
    def search(self):
        #필요물품 검색. 물품명 필요
        if self.lineEdit_13.text() != '':
            self.t1.fileExecute('query_0050.txt', {'PROD_NAME':'%' + self.lineEdit_13.text() + '%'})
    def addItem(self):
        #필요물품 추가. 테이블 더블클릭시 발생.
        tmpRow = int(self.t1.currentRow())
        if (tmpRow >= 0 and self.lineEdit_17.text() != ''):
            jjap.bt1(self, self.t1, 'query_0102.txt', {'ORD_ID':str(self.ord_id), 'PROD_ID':self.t1.item(tmpRow, 0).text(), 'ORD_REQUEST_QUANTITY':self.lineEdit_17.text(), 'DEPOSIT_DAT':''})
        elif self.lineEdit_17.text() == '':
            mb = QMessageBox(self)
            mb.setText("Error : 수량을 입력해주세요.")
            mb.show()
    def msgClicked(self, table):
        self.parent().find_id('')
        self.destroy()
class RPROD(QDialog,uic.loadUiType("ui/반품추가.ui")[0]):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.t1 = QCustomTable()
        self.t2 = QCustomTable()
        self.t1.select("WAREPROD")
        self.t2.select("DISPROD")
        self.gridLayout_12.addWidget(self.t1)
        self.gridLayout_15.addWidget(self.t2)
        self.dateEdit.setDate(datetime.date.today())
        self.t1.doubleClicked.connect(self.addItem)
        self.t2.doubleClicked.connect(self.addItem)
        self.pushButton_2.clicked.connect(self.addItem)
        
    #반품물품에 물품 추가. 테이블에서 더블클릭한 것을 추가함
    #반품물품에는 추가함과 동시에 빼내온 테이블에서는 삭제하여야함.
    def addItem(self):
        #table은 창고 혹은 진열
        if self.tabWidget.currentIndex() == 0:
            table = self.t1
            r = table.currentRow()
            n = table.item(r,1).text()
        elif self.tabWidget.currentIndex() == 1:
            table = self.t2
            r = table.currentRow()
            n = table.item(r,2).text()
        #너무 많은 반품 요구
        if int(n) < int(self.lineEdit_4.text()):
            mb = QMessageBox(self, text = '반품량이 너무 많습니다!')
            print(2)
            mb.show()
            return 0
        #반품물품에 생성
        self.parent().t5.fileExecute('query_0501.txt', {'PROD_ID':table.item(r, 0).text(),
         'RETURN_REQUEST_QUANTITY':self.lineEdit_4.text(),'RETURN_CAUSE_CODE':self.comboBox.currentText(), 
         'RETURN_DAT':str(self.dateEdit.date())})
        #창고물품 / 진열물품에서 제외
        if self.tabWidget.currentIndex() == 0:
            if n == self.lineEdit_4.text():
                table.fileExecute('query_0504.txt', {'PROD_ID':table.item(r,0).text(), 'MANUFACTURE_DAT':table.item(r,2).text()})
            else:
                table.fileExecute('query_0505.txt', {'PROD_ID':table.item(r,0).text(), 'MANUFACTURE_DAT':table.item(r,2).text(), 'QUANTITY':table.item(r,1).text()})

        elif self.tabWidget.currentIndex() == 1:
            if n == self.lineEdit_4.text():
                table.fileExecute('query_0502.txt', {'PROD_ID':table.item(r,0).text(), 'MANUFACTURE_DAT':table.item(r,3).text()})
            else:
                table.fileExecute('query_0503.txt', {'PROD_ID':table.item(r,0).text(), 'MANUFACTURE_DAT':table.item(r,3).text(), 'QUANTITY':table.item(r,2).text()})
                

        
class D_PROD(QDialog,uic.loadUiType("ui/폐기물품.ui")[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class L_PROD(QDialog,uic.loadUiType("ui/재고파악.ui")[0]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    global cursor
    cursor = access('52.79.194.219', 'team', 'team')
    
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    