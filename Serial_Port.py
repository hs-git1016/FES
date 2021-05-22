import binascii
import re
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import *

def Open_port(self):
    comName = self.Com_Name_Combo.currentText()
    comBaud = int(self.Com_Baud_Combo.currentText())
    self.com.setPortName(comName)
    try:
        if self.com.open(QSerialPort.ReadWrite) == False:
            QMessageBox.critical(self, '严重错误', '串口打开失败')
            return
    except:
        QMessageBox.critical(self, '严重错误', '串口打开失败')
        return
    self.Com_Close_Button.setEnabled(True)
    self.Com_Open_Button.setEnabled(False)
    self.Com_Refresh_Button.setEnabled(False)
    self.Com_Name_Combo.setEnabled(False)
    self.Com_Baud_Combo.setEnabled(False)
    self.Com_isOpenOrNot_Label.setText('  已打开')
    self.com.setBaudRate(comBaud)

def Close_port(self):
    self.com.close()
    self.Com_Close_Button.setEnabled(False)
    self.Com_Open_Button.setEnabled(True)
    self.Com_Refresh_Button.setEnabled(True)
    self.Com_Name_Combo.setEnabled(True)
    self.Com_Baud_Combo.setEnabled(True)
    self.Com_isOpenOrNot_Label.setText('  已关闭')

def Refresh_Port(self):
    self.Com_Name_Combo.clear()
    com = QSerialPort()
    com_list = QSerialPortInfo.availablePorts()
    for info in com_list:
        com.setPort(info)
        if com.open(QSerialPort.ReadWrite):
            self.Com_Name_Combo.addItem(info.portName())
            com.close()   
 
def Receive_information(self):
    try:
        rxData = bytes(self.com.readAll())
    except:
        QMessageBox.critical(self, '严重错误', '串口接收数据错误')
    if self.hexShowing_checkBox.isChecked() == False :
        try:
            self.textEdit_Recive.insertPlainText(rxData.decode('UTF-8'))
        except:
            pass
    else :
        Data = binascii.b2a_hex(rxData).decode('ascii')
        # re 正则表达式 (.{2}) 匹配两个字母
        hexStr = ' 0x'.join(re.findall('(.{2})', Data))
        # 补齐第一个 0x
        hexStr = '0x' + hexStr
        self.textEdit_Recive.insertPlainText(hexStr)
        self.textEdit_Recive.insertPlainText(' ')

def btnstate(self,btn):
    #输出按钮1与按钮2的状态，选中还是没选中
    if self.btn.text()== "通道1":
        if self.btn.isChecked() == True:
             print(self.btn.text()+"is selected")
        else:
            print(self.btn.text()+"is deselected")

    if self.btn.text()=="通道2":
        if self.btn.isChecked() == True:
            print(self.btn.text() + "is selected")
        else:
            print(self.btn.text() + "is deselected")


