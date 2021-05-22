import binascii  
import struct  
  
  
  
def example(express, result=None):  
    if result == None:  
        result = eval(express)  
    print(express, ' ==> ', result)  
  
print(hex(16)) 
if __name__ == '__main__':  
      
    print('整数之间的进制转换:')  
    print("10进制转16进制", end=': ');example("hex(16)")  
    print("16进制转10进制", end=': ');example("int('0x10', 16)")  
    print("类似的还有oct()， bin()")  
      
    print('\n-------------------\n')  
      
    print('字符串转整数:')  
    print("10进制字符串", end=": ");example("int('10')")  
    print("16进制字符串", end=": ");example("int('10', 16)")  
    print("16进制字符串", end=": ");example("int('0x10', 16)")  
      
    print('\n-------------------\n')  
      
    print('字节串转整数:')  
    print("转义为short型整数", end=": ");example(r"struct.unpack('<hh', bytes(b'\x01\x00\x00\x00'))")  
    print("转义为long型整数", end=": ");example(r"struct.unpack('<L', bytes(b'\x01\x00\x00\x00'))")  
  
    print('\n-------------------\n')  
  
    print('整数转字节串:')  
    print("转为两个字节", end=": ");example("struct.pack('<HH', 1,2)")  
    print("转为四个字节", end=": ");example("struct.pack('<LL', 1,2)")  
      
    print('\n-------------------\n')  
      
    print('字符串转字节串:')  
    print('字符串编码为字节码', end=": ");example(r"'12abc'.encode('ascii')")  
    print('数字或字符数组', end=": ");example(r"bytes([1,2, ord('1'),ord('2')])")  
    print('16进制字符串', end=': ');example(r"bytes().fromhex('010210')")  
    print('16进制字符串', end=': ');example(r"bytes(map(ord, '\x01\x02\x31\x32'))")  
    print('16进制数组', end =': ');example(r'bytes([0x01,0x02,0x31,0x32])')  
      
    print('\n-------------------\n')  
      
    print('字节串转字符串:')  
    print('字节码解码为字符串', end=": ");example(r"bytes(b'\x31\x32\x61\x62').decode('ascii')")  
    print('字节串转16进制表示,夹带ascii', end=": ");example(r"str(bytes(b'\x01\x0212'))[2:-1]")  
    print('字节串转16进制表示,固定两个字符表示', end=": ");example(r"str(binascii.b2a_hex(b'\x01\x0212'))[2:-1]")  
    print('字节串转16进制数组', end=": ");example(r"[hex(x) for x in bytes(b'\x01\x0212')]")  
      
      
    print('\n===================\n')  
from Ui_FES import Ui_MainWindow
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.CreateItems()
        self.CreateSignalSlot()
        self.radioButton_2.setChecked(True)
        
    def CreateItems(self):
        self.timer = QTimer(self) #初始化一个定时器
        self.timer.start(100) #设置计时间隔 100ms 并启动
    
    def CreateSignalSlot(self):
        #toggled信号与槽函数绑定
        self.radioButton.toggled.connect(lambda :self.btnstate(self.radioButton))
        self.radioButton_2.toggled.connect(lambda: self.btnstate(self.radioButton_2))

    def btnstate(self,btn):
    #输出按钮1与按钮2的状态，选中还是没选中
        if btn.text()== "通道1":
            if btn.isChecked() == True:
                print(btn.text()+"is selected")
            else:
                print(btn.text()+"is deselected")

        if btn.text()=="通道2":
            if btn.isChecked() == True:
                print(btn.text() + "is selected")
            else:
                print(btn.text() + "is deselected")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
    

















