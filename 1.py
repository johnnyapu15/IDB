import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from oracle import *
import jjap

form_class = uic.loadUiType("ui/1.ui")[0]
date =[31,28,31,30,31,30,31,31,30,31,30,31]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        
        super().__init__()
        self.setupUi(self)
        self.t1 = QCustomTable()    #EMP
        self.t2 = QCustomTable()    #PROD
        self.t3 = QCustomTable()    #필요물품
        self.t5 = QCustomTable()    #반품물품
        self.t6 = QCustomTable()    #DPROD
        self.t7 = QCustomTable()    #EVENT
        self.t8 = QCustomTable()    #ORD
        self.t9 = QCustomTable()    #BUDGET


        self.t10 = QCustomTable()   #창고물품
        self.t11 = QCustomTable()   #진열물품
        self.t12 = QCustomTable()   #판매

        self.t14 = QCustomTable()   #손실물품
    

        self.t13 = QCustomTable()   #CUSTOMER
        self.t15 = QCustomTable()   #EPROD

        self.t10.select("WAREPROD")
        self.t11.select("DISPROD")
        self.t12.select("SELL")
        self.t14.select("LPROD")
        self.t7.select("EVENT")
        self.gridLayout_11.addWidget(self.t7)
        self.gridLayout_4.addWidget(self.t14)
        self.gridLayout_9.addWidget(self.t12)
        self.gridLayout_13.addWidget(self.t10)
        self.gridLayout_14.addWidget(self.t11)
        self.gridLayout.addWidget(self.t1)
        self.t1.select("EMP")
        self.gridLayout_5.addWidget(self.t5)    #반품물품
        self.t5.select("RPROD")

        self.gridLayout_2.addWidget(self.t2)    
        self.t2.select("PROD")
        
        self.gridLayout_12.addWidget(self.t6)   #폐기물품
        self.t6.select("DPROD")
       
        self.gridLayout_15.addWidget(self.t13)
        self.t13.select("CUSTOMER")

        self.gridLayout_8.addWidget(self.t8)
        self.t8.select("ORD")

        self.gridLayout_10.addWidget(self.t9)
        self.t9.select("BUDGET")

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
        self.dateEdit_2.setDate(datetime.date.today())
        self.dateEdit_6.setDate(datetime.date.today())
        self.dateEdit_4.setDate(datetime.date.today())
        self.dateEdit_7.setDate(datetime.date.today())
        self.dateEdit_8.setDate(datetime.date.today())
        self.dateEdit_9.setDate(datetime.date.today())
        self.dateEdit_10.setDate(datetime.date.today())

        ########################

        #####반품 관련###########
        
        #반품 생성 버튼
        self.pushButton_24.clicked.connect(self.ins_RTN)
        #반품 검색버튼
        self.pushButton_38.clicked.connect(self.search_RTN)
        #반품 버튼
        self.pushButton_26.clicked.connect(self.exe_RTN)
        #반품 삭제 버튼
        self.pushButton_25.clicked.connect(self.del_RTN)
        ########################

        #####폐기 관련###########
        
        #폐기 생성 버튼
        #GUI에서 연결함.
        # self.pushButton_42.clicked.connect(self.ins_DPROD)
        #폐기 검색버튼
        self.pushButton_6.clicked.connect(self.search_DPROD)
        #폐기 삭제 버튼
        self.pushButton_43.clicked.connect(self.del_DPROD)
        ########################

        #######창고 to 진열#######
        self.t10.doubleClicked.connect(self.wareToDis)
        self.pushButton_45.clicked.connect(self.search_WareToDis)
        ########판매###############
        self.tableWidget_2.clicked.connect(self.quantity_Gui)
        self.spinBox_3.valueChanged.connect(self.quantity_Spin)
        self.pushButton_5.clicked.connect(self.del_SELL_GUI)
        self.tableWidget_2.itemChanged.connect(self.refresh_SELL)
        self.pushButton_2.clicked.connect(self.pay)
        self.pushButton_39.clicked.connect(self.refund)
        self.pushButton_49.clicked.connect(self.search_SELL)
        #############################

        ##############재고파악(손실)############
        self.pushButton_7.clicked.connect(self.search_LPROD)
        self.pushButton_36.clicked.connect(self.del_LPROD)

        #######################################
        ########################정주안 작업끝라인####################
        #####재웅 추가####
        self.pushButton_32.clicked.connect(self.call_ADD_SELLPROD)   #상품.ui 판매페이지에서
        self.pushButton_23.clicked.connect(self.call_PROD)   #상품.ui 상품목록페이지에서
        self.pushButton_42.clicked.connect(self.call_DPROD)   #폐기물품.ui 폐기처리내역페이지에서
        self.pushButton_35.clicked.connect(self.call_LPROD)   #재고파악.ui 재고파악내역페이지에서
        self.pushButton.clicked.connect(self.call_ADD_EVENT)   #이벤트생성.ui 이벤트페이지에서
        self.pushButton_4.clicked.connect(self.call_UPDATE_EVENT)   #이벤트수정.ui 이벤트페이지에서
        #결산 페이지에서 월말결산.UI 창 언제 띄워야하지
        self.pushButton_21.clicked.connect(self.call_ADD_EMP)   #직원고용.ui 직원페이지에서
        #self.pushButton_22.clicked.connect(self.call_UPDATE_EMP)   #직원수정.ui 직원페이지에서
        self.pushButton_48.clicked.connect(self.call_ROSTER)   #근무표.ui 직원페이지에서
        self.pushButton_51.clicked.connect(self.call_ADD_MEMBERSHIP)   #멤버쉽 가입.ui 멤버쉽페이지에서
        #####재웅 끝######
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)
        self.lineEdit.editingFinished.connect(self.set0)
        self.comboBox.currentIndexChanged.connect(self.selected_widget)
        self.stackedWidget.setCurrentIndex(0) #첫화면 띄우도록
        self.pushButton_23.clicked.connect(self.call_NEW_PROD)
        self.pushButton_29.clicked.connect(self.call_DEL_PROD)
        self.pushButton_40.clicked.connect(self.call_settle_account)
        self.pushButton_31.clicked.connect(self.search_emp)
        self.pushButton_21.clicked.connect(self.call_hire_employee)
        self.t1.doubleClicked.connect(self.changeEmpInfo)
        self.pushButton_22.clicked.connect(self.call_DEL_EMP)
        self.pushButton_52.clicked.connect(self.searchMembership)
        self.pushButton_20.clicked.connect(self.search_event)
        self.pushButton_33.clicked.connect(self.search_PROD)
        self.t7.doubleClicked.connect(self.showEventProd)
    def showEventProd(self):
        if self.t7.currentItem()==None:
            mb = QMessageBox(self)
            mb.setText("Error : 더블클릭해주세요.")
            mb.show()
            return
        else:
           self.t15.fileExecute('query_0009.txt',{'eventid':self.t7.item(self.t7.currentRow(),5).text()})
           self.t15.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
           self.w1 = SHOW_EVENT_PROD(self.t15,int(self.t7.item(self.t7.currentRow(),5).text()))
           self.w1.pushButton.clicked.connect(self.w1.addEventProd)
           self.w1.pushButton_2.clicked.connect(self.w1.close)
           self.w1.show()

    def timeout(self):
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        
    def set0(self): #위젯을 판매 페이지로
        self.stackedWidget.setCurrentIndex(0)   
        self.comboBox.setCurrentIndex(0)
    def selected_widget(self):
        self.stackedWidget.setCurrentIndex(self.comboBox.currentIndex())
    
    ######발주관련################
    def call_ORDPROD(self):
        self.w1 = ORD_PROD(self)
        self.w1.find_id(self.t8.item(self.t8.currentRow(), 1).text())
        self.w1.show()          
    def ins_ORD(self):
        jjap.bt1(self, self.t8, 'query_0101.txt', {'ORD_DAT':str(datetime.date.today()), 'BRANCH_ID':'1000'})
    def del_ORD(self):
        jjap.bt2(self, self.t8, 'query_0401.txt', {'ORD_ID':self.t8.item(self.t8.currentRow(), 1).text()})
    #발주 정상수령 버튼
    def dep_ORD(self):
        w1 = ORD_PROD(self)
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
    def del_RTN(self):
        jjap.bt2(self, self.t5,'query_0506.txt', {'RETURN_ID':self.t5.item(self.t5.currentRow(), 1).text()})
    #반품 버튼
    def exe_RTN(self):
        self.t5.fileExecute('query_0507.txt', {'RETURN_ID':self.t5.item(self.t5.currentRow(), 1).text(), 'PROD_ID':self.t5.item(self.t5.currentRow(), 0).text(), 'RETURN_PROCESS_RESULT':'1'})
        self.t5.refresh()
        mb = QMessageBox(self, text = self.t5.item(self.t5.currentRow(),6).text() + '가(이) 반품 진행중 처리되었습니다.')
        mb.show()
    def search_RTN(self):
        self.t5.fileExecute('query_0508.txt',{'START_DAY':self.dateEdit_2.text(), 'END_DAY':self.dateEdit_6.text()})
        
    #############################
    #####폐기 관련################
    def ins_DPROD(self):
        self.w1 = DPROD(self)
        self.w1.show()
    
    def del_DPROD(self):
        jjap.bt2(self, self.t6,'query_0603.txt', {'PROD_ID':self.t6.item(self.t6.currentRow(), 0).text(), 'DISPOSE_PROCESS_DAT':self.t6.item(self.t6.currentRow(), 2).text()})


    def search_DPROD(self):
        self.t6.fileExecute('query_0602.txt',{'START_DAY':self.dateEdit_4.text(), 'END_DAY':self.dateEdit_7.text()})
        
    #####폐기 관련끝##############
    #####창고 to 진열############
    def wareToDis(self):
        self.w1 = wareToDis_Count(self)
        self.w1.show()
    def search_WareToDis(self):
        code = self.lineEdit_22.text()
        name = self.lineEdit_23.text()
        if code != '':
            #코드로 검색
            self.t10.fileExecute('query_0053.txt', {'PROD_ID':code})
            self.t11.fileExecute('query_0054.txt', {'PROD_ID':code})
            self.hide()
        elif name != '':
            #상품명으로 검색
            self.t10.fileExecute('query_0051.txt', {'PROD_NAME':"%" + name + "%"})
            self.t11.fileExecute('query_0052.txt', {'PROD_NAME':"%" + name + "%"})
            self.hide()
        else:
            mb = QMessageBox(self, text = '상품코드 혹은 상품명을 입력하세요.')
            mb.show()
    ###############################
    ##########판매
    def quantity_Gui(self):
        self.spinBox_3.setValue(int(self.tableWidget_2.item(self.tableWidget_2.currentRow(), 4).text()))
    def quantity_Spin(self, i):
        if self.tableWidget_2.currentItem() != None:
            price = self.tableWidget_2.item(self.tableWidget_2.currentRow(), 2).text()
            dc_Unit = self.tableWidget_2.item(self.tableWidget_2.currentRow(), 6).text()
            dc_Ratio = self.tableWidget_2.item(self.tableWidget_2.currentRow(), 7).text()
            dc = int(price) * ( (i % int(dc_Unit)) + (int((i / int(dc_Unit)))*(1 - float(dc_Ratio))))
            self.tableWidget_2.setItem(self.tableWidget_2.currentRow(), 5, QTableWidgetItem(str(round(dc))))
            self.tableWidget_2.setItem(self.tableWidget_2.currentRow(), 4, QTableWidgetItem(str(i)))
    def del_SELL_GUI(self):
        if self.tableWidget_2.currentItem() != None:
            self.tableWidget_2.removeRow(self.tableWidget_2.currentRow())

    def refresh_SELL(self, item):
        if item.column() == 4:
            sum_p = 0   #합계
            sum_fin = 0 #총액
            for r in range(self.tableWidget_2.rowCount()):
                price = int(self.tableWidget_2.item(r, 2).text())
                quan = int(self.tableWidget_2.item(r, 4).text())
                r_sum = int(self.tableWidget_2.item(r, 5).text())
                sum_p += price * quan
                sum_fin += r_sum
            self.lineEdit_2.setText(str(sum_p))
            self.lineEdit_3.setText(str(sum_fin - sum_p))
            self.lineEdit_5.setText(str(sum_fin))
        #판매 테이블에 현재 tableWidget_2 를 판매물품으로써 추가한다.
    def pay(self):
        if self.tableWidget_2.rowCount() > 0:
            #판매 테이블 추가
            now = str(datetime.datetime.now())
            self.t12.fileExecute('query_0701.txt', 
            {'CUSTOMER_ID':'0','SELL_DAT':str(datetime.date.today()),
            'SELL_TIME':now})
            #판매 검색
            tmpt = QCustomTable()
            tmpt.tableName = 'SELL'
            tmpt.execute("select SELL_ID from sell where SELL_DAT = '"
            + str(datetime.date.today()) + "' and SELL_TIME = '" + now + "'")

            sell_Id = tmpt.item(0,0).text()
            #판매물품 하나하나 추가
            tmpt = QCustomTable()
            tmpt.select('disprod')
            for r in range(self.tableWidget_2.rowCount()):
                self.t12.fileExecute('query_0703.txt', 
                {'SELL_ID':sell_Id, 'PROD_ID':self.tableWidget_2.item(r, 0).text(),
                'SELL_COST':self.tableWidget_2.item(r, 5).text(),
                'QUANTITY':self.tableWidget_2.item(r, 4).text()})
                tmpt.execute('select * from disprod where PROD_ID = ' + self.tableWidget_2.item(r,0).text())
                if tmpt.item(0,0) != None:
                    n = tmpt.item(0, 2).text()
                    if n == self.tableWidget_2.item(r, 4).text():
                        self.t12.fileExecute('query_0502.txt', {'PROD_ID':self.tableWidget_2.item(r, 0).text(), 'MANUFACTURE_DAT':tmpt.item(r,3).text()})
                    else:
                        self.t12.fileExecute('query_0503.txt', {'PROD_ID':self.tableWidget_2.item(r, 0).text(), 'MANUFACTURE_DAT':tmpt.item(r,3).text(), 'DISPLAY_QUANTITY':int(n) - int(self.tableWidget_2.item(r, 4).text())})
                else:
                    mb = QMessageBox(self, text = '진열되어있지않습니다.')
                    mb.show()
                    return 0
            #추가된 판매물품의 총액을 넣음
            self.t12.fileExecute('query_0704.txt', 
            {'SELL_ID':sell_Id, 'SELL_COST':self.lineEdit_5.text()})
            self.t11.refresh()
            self.t12.refresh()
            self.tableWidget_2.setRowCount(0)
            mb = QMessageBox(self, text = '결제되었습니다!')
            mb.show()
            
    def refund(self):
        #39푸시
        if self.t12.currentItem() != None:
            cost = int(self.t12.item(self.t12.currentRow(), 3).text())
            cost = -cost
            self.t12.fileExecute('query_0801.txt', 
            {'SELL_DAT':str(datetime.date.today()),
                'SELL_TIME':str(datetime.datetime.now()), 'SELL_COST':str(cost)})
            mb = QMessageBox(self, text = '환불처리되었습니다.')
            mb.show()
            self.t12.refresh()
    def search_SELL(self):
        if self.lineEdit_14.text() != '':
            self.t12.fileExecute('query_0705.txt', 
            {'SELL_ID':self.lineEdit_14.text()})
        else:
            mb = QMessageBox(self, text = '판매코드를 입력하세요.')
            mb.show()
    #########판매끝
    ########################손실물품관련########################
    def search_LPROD(self):
        self.t14.fileExecute('query_0901.txt',{'START_DAY':self.dateEdit_4.text(), 'END_DAY':self.dateEdit_7.text()})
    def del_LPROD(self):
        if self.t14.currentItem() != None:
            r = self.t14.currentRow()
            self.t14.fileExecute('query_0902.txt', 
            {'PROD_ID':self.t14.item(r,0).text(),
            'INVEST_DAT':self.t14.item(r,3).text(),
            'INVEST_NO':self.t14.item(r,4).text(),
            'LOSS_CAUSE_CODE':self.t14.item(r,2).text()})
            self.t14.refresh()

    ####################################################
###재웅 추가### 
    def call_ADD_SELLPROD(self):
        self.w1 = ADD_SELLPROD(self)
        self.w1.show()  
    def call_PROD(self):
        self.w1 = PROD()
        self.w1.show()    
    def call_DPROD(self):
        self.w1 = DPROD(self)
        self.w1.show()    

    def call_LPROD(self):
        self.w1 = LPROD(self)
        self.w1.show()  
    def call_ADD_EVENT(self):
        self.w1 = ADD_EVENT(self.t7)
        self.w1.pushButton_21.clicked.connect(self.w1.addevent)
        self.w1.show()  
    def call_UPDATE_EVENT(self):
        self.w1 = UPDATE_EVENT()
        self.w1.show()
    def call_ADD_EMP(self):
        self.w1 = ADD_EMP()
        self.w1.show()      
    def call_UPDATE_EMP(self):
        self.w1 = UPDATE_EMP()
        self.w1.show()    
    def call_ROSTER(self):
        self.w1 = ROSTER()
        self.w1.pushButton_6.clicked.connect(self.w1.search_roaster)
        self.w1.pushButton.clicked.connect(self.w1.startwork)
        self.w1.pushButton_2.clicked.connect(self.w1.endwork)
        self.w1.show()          
    def call_ADD_MEMBERSHIP(self):
        self.w1 = ADD_MEMBERSHIP(self.t13)
        self.w1.pushButton_21.clicked.connect(self.w1.registerMembership)
        self.w1.show()      
####재웅 끝####
####수환 시작####    
    def call_NEW_PROD(self):
        self.w1=NEW_PROD(self.t2)
        self.w1.pushButton.clicked.connect(self.w1.close)
        self.w1.pushButton_21.clicked.connect(self.w1.addNewProduct)
        self.w1.show()
    def call_DEL_PROD(self):
        if self.t2.currentItem()!=None:
            jjap.bt2(self,self.t2,'query_1301.txt',{'ProdID':self.t2.item(self.t2.currentRow(), 0).text()})
    def call_DEL_EMP(self):
        if self.t1.currentItem()!=None:
            jjap.bt2(self,self.t1,'query_1701.txt',{'EMPID':self.t1.item(self.t1.currentRow(),1).text()})

    def call_settle(self,mb):
        if mb.clickedButton().text() == "예":
            dic = {'BRANCHID':jjap.BRAN_ID,'DAT':self.dateEdit_11.text()}
            dic2 = {'DAT':self.dateEdit_11.text()}
            self.t9.fileExecute('query_1401.txt',dic)
            self.t9.fileExecute('query_1402.txt',dic2)
            self.t9.fileExecute('query_1403.txt',dic2)
            self.t9.fileExecute('query_1404.txt',dic2)
            self.t9.refresh()
        else:
            mb.close()
    def call_lastday_settle(self,mb):
        if mb.clickedButton().text() == "예":
            self.w1 = LASTDAY_SETTLE(self.t9,self.dateEdit_11.date())
            self.w1.pushButton_20.clicked.connect(self.w1.executeSettle)
            self.w1.pushButton_21.clicked.connect(self.w1.close)
            self.w1.show()
        else:
            mb.close()

    def call_settle_account(self):
        if date[self.dateEdit_11.date().month()-1]==self.dateEdit_11.date().day():
            mb = QMessageBox(self)
            mb.setText('월말입니다. 이번달 정산이 모두 완료되었는지 확인하십시요\n이작업은 되돌릴 수 없습니다! 실행하시겠습니까?')
            mb.addButton('예', 5)
            mb.addButton('아니오', 6)
            mb.show()
            mb.buttonClicked.connect(lambda:self.call_lastday_settle(mb))
  
        else:
           mb = QMessageBox(self)
           mb.setText('선택한 날짜로 결산합니다. 하시겠습니까?')
           mb.addButton('예', 5)
           mb.addButton('아니오', 6)
           mb.show()
           mb.buttonClicked.connect(lambda:self.call_settle(mb))
    def search_emp(self):
        empid = self.lineEdit_20.text()
        empname = self.lineEdit_21.text()
        if empid !="" and empname !="":
            self.t1.fileExecute('query_0000.txt',{'empid':empid,'empname':empname})
        elif empid!="":
            self.t1.fileExecute('query_0001.txt',{'empid':empid})
        elif empname!="":
            self.t1.fileExecute('query_0002.txt',{'empname':empname})
        else:
            mb = QMessageBox(self)
            mb.setText('아이디나 이름을 입력해주세요')
            mb.addButton('확인', 1)
            mb.buttonClicked.connect(mb.close)
            mb.show()
    def call_hire_employee(self):
        self.w1=HIRE_EMP(self.t1)
        self.w1.pushButton_22.clicked.connect(self.w1.close)
        self.w1.pushButton_21.clicked.connect(self.w1.hireEmployee)
        self.w1.show()
    def changeEmpInfo(self):
       if self.t1.currentItem()==None:
            mb = QMessageBox(self)
            mb.setText("Error : 더블클릭해주세요.")
            mb.show()
       else:
           self.w1 = CHANGEEMPINFO(self.t1)
           self.w1.lineEdit_6.setText(self.t1.item(self.t1.currentRow(),1).text())
           self.w1.lineEdit_7.setText(self.t1.item(self.t1.currentRow(),3).text())
           self.w1.comboBox.setCurrentIndex(int(self.t1.item(self.t1.currentRow(),2).text()))
           self.w1.lineEdit_9.setText("" if self.t1.item(self.t1.currentRow(),4).text()=='0' else self.t1.item(self.t1.currentRow(),4).text())
           self.w1.comboBox_2.setCurrentIndex(int(self.t1.item(self.t1.currentRow(),5).text()))
           self.w1.lineEdit_11.setText("" if self.t1.item(self.t1.currentRow(),6).text()=='0' else self.t1.item(self.t1.currentRow(),6).text())
           self.w1.pushButton_21.clicked.connect(self.w1.changeInfo)
           self.w1.pushButton_22.clicked.connect(self.w1.close)
           self.w1.show()
    def searchMembership(self):
        name = self.lineEdit_9.text()
        id = self.lineEdit_10.text()

        if id !="" and name !="":
            self.t13.fileExecute('query_0004.txt',{'customerid':id,'customername':name})
        elif id!="":
            self.t13.fileExecute('query_0005.txt',{'customerid':id})
        elif name!="":
            self.t13.fileExecute('query_0006.txt',{'customername':name})
        else:
            mb = QMessageBox(self)
            mb.setText('아이디나 이름을 입력해주세요')
            mb.addButton('확인', 1)
            mb.buttonClicked.connect(mb.close)
            mb.show()
    def search_event(self):
        date=self.dateEdit_10.text()
        name=self.lineEdit_13.text()

        if(name!=''):
            self.t7.fileExecute('query_0007.txt',{'DAT':date,'NAME':name})
        else:
            self.t7.fileExecute('query_0008.txt',{'DAT':date})
    def search_PROD(self):
        code = self.lineEdit_18.text()
        name = self.lineEdit_19.text()
        if code != '':
            #코드로 검색
            self.t2.fileExecute('query_0055.txt', {'PROD_ID':code})
        elif name != '':
            #상품명으로 검
            self.t2.fileExecute('query_0050.txt', {'PROD_NAME':name })
        else:
            mb = QMessageBox(self, text = '상품코드 혹은 상품명을 입력하세요.')
            mb.show()
        if self.t1.rowCount() == 0:
            mb = QMessageBox(self, text = '진열된 해당 상품이 없습니다!')
            mb.show()



            
  ####수환 끝

    #버튼이 클릭되었을 때 해당 테이블을 리프레쉬합니다.
    def msgClicked(self, table):
        table.refresh()

class ORD_PROD(QDialog,uic.loadUiType("ui/필요물품.ui")[0]):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.t1 = QCustomTable()
        self.t1.select('ORDPROD')
        self.gridLayout_10.addWidget(self.t1)
        self.ord_id = 0
        self.finished.connect(self.dest)
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
        self.t1.fileExecute("query_0103.txt", {'ORD_ID':str(self.ord_id)})
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
    def dest(self, i):
        self.parent().t8.refresh()
        self.parent().t10.refresh()
        

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
            jjap.bt1(self, self.t1, 'query_0102.txt', 
            {'ORD_ID':str(self.ord_id), 'PROD_ID':self.t1.item(tmpRow, 0).text(), 
            'ORD_REQUEST_QUANTITY':self.lineEdit_17.text(), 'DEPOSIT_DAT':''})
            
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
        self.comboBox.addItem('00')
        self.comboBox.addItem('01')
    #반품물품에 물품 추가. 테이블에서 더블클릭한 것을 추가함
    #반품물품에는 추가함과 동시에 빼내온 테이블에서는 삭제하여야함.
    def addItem(self):
        #table은 창고 혹은 진열
        #테이블 선택 안했을 때 예외처리
        if self.tabWidget.currentIndex() == 0:
            table = self.t1
            if table.currentItem() == None:
                mb = QMessageBox(self, text = '물품을 선택해주세요!')
                mb.show()
                return 0
            r = table.currentRow()
            n = table.item(r,1).text()
        elif self.tabWidget.currentIndex() == 1:
            table = self.t2
            if table.currentItem() == None:
                mb = QMessageBox(self, text = '물품을 선택해주세요!')
                mb.show()
                return 0
            r = table.currentRow()
            n = table.item(r,2).text()
        #입력 부족
        if self.lineEdit_4.text() == '':
            mb = QMessageBox(self, text = '반품량을 적어주세요!')
            mb.show()
            return 0
        #너무 많은 반품 요구
        if int(n) < int(self.lineEdit_4.text()):
            mb = QMessageBox(self, text = '반품량이 너무 많습니다!')
            mb.show()
            return 0
        #반품물품에 생성
        self.parent().t5.fileExecute('query_0501.txt', {'PROD_ID':table.item(r, 0).text(),
         'RETURN_REQUEST_QUANTITY':self.lineEdit_4.text(),'RETURN_CAUSE_CODE':self.comboBox.currentText(), 
         'RETURN_DAT':str(self.dateEdit.date().toString(Qt.ISODate))})
        self.parent().t5.refresh()
        #창고물품 / 진열물품에서 제외
        if self.tabWidget.currentIndex() == 0:
            if n == self.lineEdit_4.text():
                table.fileExecute('query_0504.txt', {'PROD_ID':table.item(r,0).text(), 'MANUFACTURE_DAT':table.item(r,2).text()})
            else:
                table.fileExecute('query_0505.txt', {'PROD_ID':table.item(r,0).text(), 'MANUFACTURE_DAT':table.item(r,2).text(), 'QUANTITY':int(n) - int(self.lineEdit_4.text())})

        elif self.tabWidget.currentIndex() == 1:
            if n == self.lineEdit_4.text():
                table.fileExecute('query_0502.txt', {'PROD_ID':table.item(r,0).text(), 'MANUFACTURE_DAT':table.item(r,3).text()})
            else:
                table.fileExecute('query_0503.txt', {'PROD_ID':table.item(r,0).text(), 'MANUFACTURE_DAT':table.item(r,3).text(), 'DISPLAY_QUANTITY':int(n) - int(self.lineEdit_4.text())})
        self.hide()
    def search(self):
        #물품 검색. 물품명 필요
        if self.lineEdit_3.text() != '':
            self.t1.fileExecute('query_0051.txt', {'PROD_NAME':'%' + self.lineEdit_3.text() + '%'})
            self.t2.fileExecute('query_0052.txt', {'PROD_NAME':'%' + self.lineEdit_3.text() + '%'})



#####재웅 추가#####
class ADD_SELLPROD(QDialog,uic.loadUiType("ui/판매상품.ui")[0]):
    def __init__(self, parent):
        super().__init__(parent) 
        self.setupUi(self)
        self.pushButton_7.clicked.connect(self.search_PROD)
        self.t1 = QCustomTable()
        self.t2 = QCustomTable()
        self.t1.select('DISPROD')
        self.gridLayout_8.addWidget(self.t1)
        self.t1.doubleClicked.connect(self.addItem)
        
    def search_PROD(self):
        code = self.lineEdit_18.text()
        name = self.lineEdit_19.text()
        if code != '':
            #코드로 검색
            self.t1.fileExecute('query_0054.txt', {'PROD_ID':code})
            self.t2.fileExecute('query_0055.txt', {'PROD_ID':code})

        elif name != '':
            #상품명으로 검색
            self.t1.fileExecute('query_0052.txt', {'PROD_NAME':name })
            self.t2.fileExecute('query_0050.txt', {'PROD_NAME':name })

        else:
            mb = QMessageBox(self, text = '상품코드 혹은 상품명을 입력하세요.')
            mb.show()
        if self.t1.rowCount() == 0:
            mb = QMessageBox(self, text = '진열된 해당 상품이 없습니다!')
            mb.show()

    def addItem(self):
        prod_Row = self.t1.currentRow()
        code = self.t1.item(prod_Row, 0).text()
        name = self.t1.item(prod_Row, 5).text()
        event_Id = self.t1.item(prod_Row, 1).text()
        self.t2.fileExecute('query_0055.txt', {'PROD_ID':code})
        price = self.t2.item(0, 5).text()

        self.t2.fileExecute('query_0056.txt', {'TODAY':datetime.date.today(), 'EVENT_ID':event_Id})
        if self.t2.rowCount() == 0:
            dc_Unit = 1
            dc_Ratio = 0
        else:
            dc_Unit = self.t2.item(0, 0).text()
            dc_Ratio = self.t2.item(0, 1).text()
        
        dc = int(price) * ( (1 % int(dc_Unit)) + (int((1 / int(dc_Unit)))*(1 - float(dc_Ratio))))
        dc = round(dc)
        r = self.parent().tableWidget_2.rowCount()
        self.parent().tableWidget_2.setRowCount(r + 1)
        self.parent().tableWidget_2.setItem(r, 0, QTableWidgetItem(code))
        self.parent().tableWidget_2.setItem(r, 1, QTableWidgetItem(name))
        self.parent().tableWidget_2.setItem(r, 2, QTableWidgetItem(price))
        self.parent().tableWidget_2.setItem(r, 3, QTableWidgetItem(str(dc)))
        self.parent().tableWidget_2.setItem(r, 5, QTableWidgetItem(str(dc)))
        self.parent().tableWidget_2.setItem(r, 6, QTableWidgetItem(str(dc_Unit)))
        self.parent().tableWidget_2.setItem(r, 7, QTableWidgetItem(str(dc_Ratio)))
        self.parent().tableWidget_2.setItem(r, 4, QTableWidgetItem('1'))
        self.hide()

        
class PROD(QDialog,uic.loadUiType("ui/상품.ui")[0]):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.call_ADD_PROD)   #상품추가.ui
    def call_ADD_PROD(self):
        self.w2 = ADD_PROD()
        self.w2.show()   

class ADD_PROD(QDialog,uic.loadUiType("ui/상품추가.ui")[0]):
    def __init__(self):
        super().__init__() 
        self.setupUi(self)        
class DPROD(QDialog,uic.loadUiType("ui/폐기물품.ui")[0]):
    def __init__(self, parent):
        super().__init__(parent) 
        self.setupUi(self)
        self.t1 = QCustomTable()
        self.t2 = QCustomTable()
        self.gridLayout_12.addWidget(self.t1)
        self.gridLayout_15.addWidget(self.t2)
        self.t1.doubleClicked.connect(self.addItem)
        self.t1.doubleClicked.connect(self.addItem)
        self.pushButton_2.clicked.connect(self.addItem)
        self.pushButton_6.clicked.connect(self.search)
        self.t1.select("WAREPROD")
        self.t2.select("DISPROD")
        self.dateEdit.setDate(datetime.date.today())

    def addItem(self):
        #table은 창고 혹은 진열
        #테이블 선택 안했을 때 예외처리
        if self.tabWidget.currentIndex() == 0:
            table = self.t1
            if table.currentItem() == None:
                mb = QMessageBox(self, text = '물품을 선택해주세요!')
                mb.show()
                return 0
            r = table.currentRow()
            n = table.item(r,1).text()
        elif self.tabWidget.currentIndex() == 1:
            table = self.t2
            if table.currentItem() == None:
                mb = QMessageBox(self, text = '물품을 선택해주세요!')
                mb.show()
                return 0
            r = table.currentRow()
            n = table.item(r,2).text()
        #입력 부족
        if self.lineEdit_17.text() == '':
            mb = QMessageBox(self, text = '폐기수량을 적어주세요!')
            mb.show()
            return 0
        #너무 많은 폐기 요구
        if int(n) < int(self.lineEdit_17.text()):
            mb = QMessageBox(self, text = '폐기수량이 너무 많습니다!')
            mb.show()
            return 0
        #폐기물품에 생성
        self.parent().t6.fileExecute('query_0601.txt', {'PROD_ID':table.item(r, 0).text(),
         'QUANTITY':self.lineEdit_17.text(), 'DISPOSE_PROCESS_DAT':str(self.dateEdit.date().toString(Qt.ISODate))})
        self.parent().t6.refresh()
        #창고물품 / 진열물품에서 제외
        if self.tabWidget.currentIndex() == 0:
            if n == self.lineEdit_17.text():
                table.fileExecute('query_0504.txt', {'PROD_ID':table.item(r,0).text(), 'MANUFACTURE_DAT':table.item(r,2).text()})
            else:
                table.fileExecute('query_0505.txt', {'PROD_ID':table.item(r,0).text(), 'MANUFACTURE_DAT':table.item(r,2).text(), 'QUANTITY':int(n) - int(self.lineEdit_17.text())})

        elif self.tabWidget.currentIndex() == 1:
            if n == self.lineEdit_17.text():
                table.fileExecute('query_0502.txt', {'PROD_ID':table.item(r,0).text(), 'MANUFACTURE_DAT':table.item(r,3).text()})
            else:
                table.fileExecute('query_0503.txt', {'PROD_ID':table.item(r,0).text(), 'MANUFACTURE_DAT':table.item(r,3).text(), 'DISPLAY_QUANTITY':int(n) - int(self.lineEdit_17.text())})
        self.hide()
    def search(self):
        #유통기한 기준 검색.
        if self.lineEdit_18.text() == '':
            self.t1.fileExecute('query_0604.txt', {'EXPIRATION_DAT':self.dateEdit.text(), 'STD_DAT':self.lineEdit_18.text()})
            self.t2.fileExecute('query_0605.txt', {'EXPIRATION_DAT':self.dateEdit.text(), 'STD_DAT':self.lineEdit_18.text()})
        else:
            mb = QMessageBox(self, text = '검색 기준일을 바르게 설정하세요.')
            mb.show()
class LPROD(QDialog,uic.loadUiType("ui/재고파악.ui")[0]):
    def __init__(self, parent):
        super().__init__(parent) 
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.addItem)   #손실내용수정.ui
        self.t1 = QCustomTable()
        self.t2 = QCustomTable()
        self.t1.select('WAREPROD')
        self.t2.select('DISPROD')
        self.gridLayout_12.addWidget(self.t1)
        self.gridLayout_15.addWidget(self.t2)
 
    def addItem(self):
        if self.lineEdit_4.text() == '':
            mb = QMessageBox(self, text = '수량을 입력하세요.')
            mb.show()
            return 0
        elif self.tabWidget.currentIndex() == 0:
            if self.t1.currentItem() == None:
                mb = QMessageBox(self, text = '물품을 선택하세요.')
                mb.show()
                return 0
            else:
                table = self.t1
                r =self.t1.currentRow()
                prodid = self.t1.item(r, 0).text()
                n = table.item(r,1).text()
        elif self.tabWidget.currentIndex() == 1:
            if self.t2.currentItem() == None:
                mb = QMessageBox(self, text = '물품을 선택하세요.')
                mb.show()
                return 0  
            else:
                table = self.t2
                r = self.t2.currentRow()
                prodid = self.t2.item(r, 0).text()
                n = table.item(r,2).text()
        
        ivdat = datetime.date.today()
        ivno = self.comboBox_5.currentText()
        loss = self.comboBox.currentText()
        quan = self.lineEdit_4.text()
        
        if int(quan) > int(n):
            mb = QMessageBox(self, text = '수량을 적절히 입력하세요.')
            mb.show()
            return 0 
        #손실물품에 추가
        self.parent().t14.fileExecute('query_0903.txt', 
        {'PROD_ID':prodid, 'INVEST_DAT':ivdat, 'INVEST_NO':ivno,
        'LOSS_CAUSE_CODE':loss, 'QUANTITY':quan})
        #창고물품 / 진열물품에서 제외
        if self.tabWidget.currentIndex() == 0:
            if n == quan:
                table.fileExecute('query_0504.txt', {'PROD_ID':prodid, 'MANUFACTURE_DAT':table.item(r,2).text()})
            else:
                table.fileExecute('query_0505.txt', {'PROD_ID':prodid, 'MANUFACTURE_DAT':table.item(r,2).text(), 'QUANTITY':int(n) - int(quan)})

        elif self.tabWidget.currentIndex() == 1:
            if n == quan:
                table.fileExecute('query_0502.txt', {'PROD_ID':prodid, 'MANUFACTURE_DAT':table.item(r,3).text()})
            else:
                table.fileExecute('query_0503.txt', {'PROD_ID':prodid, 'MANUFACTURE_DAT':table.item(r,3).text(), 'DISPLAY_QUANTITY':str(int(n) - int(quan))})
        self.hide()
        self.parent().t14.refresh()
        
        
    def search(self):
        #물품 검색. 물품명 필요
        if self.lineEdit_3.text() != '':
            self.t1.fileExecute('query_0051.txt', {'PROD_NAME':'%' + self.lineEdit_3.text() + '%'})
            self.t2.fileExecute('query_0052.txt', {'PROD_NAME':'%' + self.lineEdit_3.text() + '%'})


        
        
class ADD_EVENT(QDialog,uic.loadUiType("ui/이벤트 생성.ui")[0]):
    def __init__(self,table):
        super().__init__() 
        self.setupUi(self)
        self.lineEdit_7.setValidator(QtGui.QIntValidator())
        self.table = table
    def addevent(self):
        name = self.lineEdit_6.text()
        unit = 0 if self.lineEdit_7.text()=='' else int(self.lineEdit_7.text())
        ratio = 0.0 if self.lineEdit_8.text()=='' else float(self.lineEdit_8.text())
        startdat = self.dateEdit.text()
        enddat = self.dateEdit_2.text()
        if(name=='' or unit==0 or ratio ==0.0 ):
            mb = QMessageBox(self, text = '모든 항목을 입력해주셔야 합니다.')
            mb.show()
            return
        dic = {'NAME':name,'UNIT':unit,'RATIO':ratio,'STARTDAT':startdat,'ENDDAT':enddat}
        jjap.bt1(self,self.table,'query_2201.txt',dic)
    def msgClicked(self, table):
        table.refresh()

    
class UPDATE_EVENT(QDialog,uic.loadUiType("ui/이벤트 수정.ui")[0]):
    def __init__(self):
        super().__init__() 
        self.setupUi(self)
class ADD_EMP(QDialog,uic.loadUiType("ui/직원고용.ui")[0]):
    def __init__(self):
        super().__init__() 
        self.setupUi(self)
class UPDATE_EMP(QDialog,uic.loadUiType("ui/직원수정.ui")[0]):
    def __init__(self):
        super().__init__() 
        self.setupUi(self)        
class ROSTER(QDialog,uic.loadUiType("ui/근무표.ui")[0]):
    def __init__(self):
        super().__init__() 
        self.setupUi(self)
        self.table = QCustomTable()
        self.gridLayout_11.addWidget(self.table)
        self.table.select('ROSTER')
        self.lineEdit_14.setValidator(QtGui.QIntValidator())
    def search_roaster(self):
        dic = {'EMPID':self.lineEdit_14.text()}
        self.table.fileExecute('query_0003.txt',dic)
    def startwork(self):
        if(self.lineEdit_14.text()==""):
            return
        dic = {'EMPID':self.lineEdit_14.text()}
        self.table.fileExecute('query_1901.txt',dic)
    def endwork(self):
        if(self.lineEdit_14.text()==""):
             return
        dic = {'EMPID':self.lineEdit_14.text()}
        self.table.fileExecute('query_2001.txt',dic)

    def msgClicked(self, table):
        table.refresh()

    
    
class ADD_MEMBERSHIP(QDialog,uic.loadUiType("ui/멤버쉽 가입.ui")[0]):
    def __init__(self,table):
        super().__init__() 
        self.setupUi(self)
        self.lineEdit_13.setValidator(QtGui.QIntValidator())
        self.table =table
    def registerMembership(self):
        name = self.lineEdit_6.text()
        gender = 0 if self.comboBox.currentText()=='남자' else 1
        age = int(0 if self.lineEdit_13.text()=='' else self.lineEdit_13.text())
        if(name=='' or age ==0):
            mb = QMessageBox(self, text = '이름과 나이를 입력해주세요')
            mb.show()
            return
        dic = {'customername':name,'gender':gender,'age':age}
        jjap.bt1(self,self.table,'query_2101.txt',dic)
    def msgClicked(self, table):
         table.refresh()




####재웅 끝#####        

class wareToDis_Count(QDialog,uic.loadUiType("ui/창고to진열 수량 결정.ui")[0]):
    def __init__(self, parent):
        super().__init__(parent) 
        self.setupUi(self) 
        self.pushButton_20.clicked.connect(self.ok)

    def ok(self):
        PRODID = self.parent().t10.item(self.parent().t10.currentRow(), 0).text()
        MAN_DAT = self.parent().t10.item(self.parent().t10.currentRow(), 2).text()
        QUAN = self.parent().t10.item(self.parent().t10.currentRow(), 1).text()
        QUAN_ORD = self.lineEdit.text()
        if QUAN_ORD == '':
            mb = QMessageBox(self, text = '수량을 입력하세요.')
            mb.show()
        else:
            #진열물품에 해당 물품이 존재할 경우
            self.tmpt = QCustomTable()
            self.tmpt.tableName = 'DISPROD'
            self.tmpt.execute('select * from disprod where PROD_ID = ' + 
                        PRODID + "AND MANUFACTURE_DAT = '" + MAN_DAT + "'")
            if self.tmpt.rowCount() > 0:
                self.parent().t10.fileExecute('query_1107.txt',
                {'PROD_ID':str(PRODID),
                'MANUFACTURE_DAT':str(MAN_DAT), 'QUANTITY':QUAN_ORD})
            #진열되어있지 않으면 새로 생성
            else:
                self.parent().t10.fileExecute('query_1108.txt',
                    {'PROD_ID':str(PRODID),
                    'MANUFACTURE_DAT':str(MAN_DAT), 
                    'QUANTITY':QUAN_ORD})
            #정상. 실 수량 > 요구 수량 -> 창고 수정
            if int(QUAN) < int(QUAN_ORD):
                mb = QMessageBox(self, text = '수량이 너무 많습니다.')
                mb.show()
                return 0
            if int(QUAN) > int(QUAN_ORD):
                self.parent().t10.fileExecute('query_1106.txt',
                {'PROD_ID':str(PRODID),
                'MANUFACTURE_DAT':str(MAN_DAT), 'QUANTITY':str(int(QUAN) - int(QUAN_ORD))})
                
            else:
                self.parent().t10.fileExecute('query_1105.txt',
                {'PROD_ID':str(PRODID),
                'MANUFACTURE_DAT':str(MAN_DAT)})
            
            
            self.parent().t10.refresh()
            self.parent().t11.refresh()
            self.hide()
                

        
####수환 시작####
class SHOW_EVENT_PROD(QDialog,uic.loadUiType("ui/이벤트물품.ui")[0]):
    def __init__(self,table,id):
        super().__init__()
        self.setupUi(self)
        self.table =table
        self.id =id
        self.gridLayout.addWidget(self.table)
    def addEventProd(self):
        self.w1=ADD_EVENT_PROD(self.table,self.id)
        self.w1.pushButton_21.clicked.connect(self.w1.addEprod)
        self.w1.show()

class ADD_EVENT_PROD(QDialog,uic.loadUiType("ui/이벤트물품추가.ui")[0]):
    def __init__(self,table,id):
        super().__init__()
        self.setupUi(self)
        self.id=id
        self.table=table
        self.table.tableName='EPROD'
        self.lineEdit_8.setValidator(QtGui.QIntValidator())
    def addEprod(self):
        if(self.lineEdit_8.text()==''):
            mb = QMessageBox(self, text = '모든 칸을 채워야 합니다!')
            mb.show()
            return 0
        prodid =self.lineEdit_8.text()
        dic={'PRD':prodid,'EVD':self.id}
        jjap.bt1(self,self.table,"query_2202.txt",dic)
        self.close()
    def msgClicked(self, table):
          table.fileExecute('query_0009.txt',{'eventid':self.id})
          table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

class CHANGEEMPINFO(QDialog,uic.loadUiType("ui/직원수정.ui")[0]):
    def __init__(self,table):
        super().__init__()
        self.setupUi(self)
        self.lineEdit_9.setValidator(QtGui.QIntValidator())
        self.lineEdit_11.setValidator(QtGui.QIntValidator())
        self.table=table
    def changeInfo(self):
        dic = {'GRADECODE': 0 if self.comboBox.currentText()=='점장' else 1,'NAME':self.lineEdit_7.text(),'CONTACT':self.lineEdit_9.text(),
        'SALARY_CODE':0 if self.comboBox_2.currentText()=='연봉' else 1 if self.comboBox_2.currentText()=='월급'else 2,'SALARY':int(self.lineEdit_11.text()),'EMPID':self.lineEdit_6.text()}
        print(dic)
        jjap.bt3(self,self.table,'query_1801.txt',dic)

    def msgClicked(self, table):
         table.refresh()

        
class LASTDAY_SETTLE(QDialog,uic.loadUiType('ui/월말결산.ui')[0]):
    def __init__(self,table,date):
        super().__init__()
        self.setupUi(self)
        self.lineEdit.setValidator(QtGui.QIntValidator())
        self.table = table
        self.dat =date

    def executeSettle(self):
            dic = {'BRANCHID':jjap.BRAN_ID,'DAT':date}
            dic2 = {'DAT':self.dat}
            dic3 = {'DAT':date,'UPKEEP':self.lineEdit.text()}
            self.table.fileExecute('query_1501.txt',dic)
            self.table.fileExecute('query_1502.txt',dic2)
            self.table.fileExecute('query_1503.txt',dic2)
            self.table.fileExecute('query_1504.txt',dic2)
            self.table.fileExecute('query_1505.txt',dic3)
            self.table.fileExecute('query_1506.txt',dic2)
            self.emptable = QCustomTable()
            self.emptable.execute('SELECT EMP_ID FROM EMP WHERE SALARY_CODE = 2')
            
            dic3 = {}
            self.table.fileExecute('query_1508.txt',dic2)
            self.table.fileExecute('query_1509.txt',dic2)
            self.table.fileExecute('query_1510.txt',dic2)
            self.table.fileExecute('query_1511.txt',dic2)
            self.table.fileExecute('query_1512.txt',dic2)
            self.table.fileExecute('query_1513.txt',dic2)
            self.table.fileExecute('query_1514.txt',dic2)

class NEW_PROD(QDialog,uic.loadUiType("ui/상품추가.ui")[0]):
      def __init__(self,table):
        super().__init__()
        self.setupUi(self)
        self.lineEdit_13.setValidator(QtGui.QIntValidator())
        self.lineEdit_9.setValidator(QtGui.QIntValidator())
        self.lineEdit_10.setValidator(QtGui.QIntValidator())
        self.lineEdit_12.setValidator(QtGui.QIntValidator())
        self.table = table
        
      def addNewProduct(self):
          if self.lineEdit_6.text() == "" or self.lineEdit_13.text()=="" or self.lineEdit_9.text()=="" or self.lineEdit_10.text()=="" or self.lineEdit_12.text() == "":
              mb = QMessageBox(self, text = '모든 칸을 채워야 합니다!')
              mb.show()
              return 0

          dic = {'NAME':self.lineEdit_6.text(),'MAINC':int(self.comboBox.currentText()),'SUBC':int(self.comboBox_2.currentText()),'CUST':int(self.lineEdit_13.text()),
          'SELL':int(self.lineEdit_9.text()),'DIST':int(self.lineEdit_10.text()),'EXCL':('1' if self.checkBox.isChecked() else '0'),'BUYP':int(self.lineEdit_12.text())}
          if dic['SELL']<=0 or dic['CUST']<=0 or dic['BUYP']<=0:
              mb = QMessageBox(self, text = '가격은 0이상이여야 합니다.')
              mb.show()
              return 0
          print (dic)
          jjap.bt1(self,self.table,'query_1201.txt',dic)
      def msgClicked(self, table):
         table.refresh()
class HIRE_EMP(QDialog,uic.loadUiType("ui/직원고용.ui")[0]):
    def __init__(self,table):
        super().__init__()
        self.setupUi(self)
        self.lineEdit_9.setValidator(QtGui.QIntValidator())
        self.lineEdit_11.setValidator(QtGui.QIntValidator())
        self.table =table
    def hireEmployee(self):
        if self.lineEdit_7.text()=="":
            mb = QMessageBox(self, text = '이름은 필수 항목입니다!')
            mb.show()
            return
        else:
            dic={'BRANCH_ID':jjap.BRAN_ID,'EMPGRADE': 0 if self.comboBox.currentText()=='점장' else 1,'EMPNAME':self.lineEdit_7.text(),'CONTACT': '0' if self.lineEdit_9.text() == "" else self.lineEdit_9.text(),
            'SALARY_CODE':0 if self.comboBox_2.currentText()=='연봉' else 1 if self.comboBox_2.currentText()=='월급' else 2,'SALARY':0 if self.lineEdit_11.text() =="" else int(self.lineEdit_11.text())}
            print(dic)
            jjap.bt1(self, self.table,'query_1601.txt',dic)
            self.close()
    
    def msgClicked(self, table):
        table.refresh()

            

#### 수환 끝 ####


        

if __name__ == "__main__":
    global cursor
    cursor = access('52.79.194.219', 'team', 'team')
    
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
    