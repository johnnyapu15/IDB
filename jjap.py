from PyQt5.QtWidgets import *
from PyQt5 import uic
import datetime

BRAN_ID = 1000

def bt1(sf, table, query, dic):
    #추가 요청
    mb = QMessageBox(sf)
    mb.setText('추가하시겠습니까?')
    mb.addButton("예", 5)
    mb.addButton("아니오", 6)
    mb.buttonClicked.connect(lambda: execute(mb, table, query, dic))
    mb.show()
    try:
        mb.buttonClicked.connect(lambda: sf.msgClicked(table))
        #mb.destroy()
    except:
        print('연결오류')
def bt2(sf, table, query, dic):
    #삭제 요청
    mb = QMessageBox(sf)
    mb.setText("삭제하시겠습니까?")
    mb.addButton('예', 5)
    mb.addButton('아니오', 6)
    mb.show()
    mb.buttonClicked.connect(lambda: execute(mb, table, query, dic))
    try:
        mb.buttonClicked.connect(lambda: sf.msgClicked(table))
    except:
        print('연결오류')
def execute(sf, table, query, dic):
    if sf.clickedButton().text() == "예":
        table.fileExecute(query, dic)
        sf.destroy()
    else:
        sf.destroy()

