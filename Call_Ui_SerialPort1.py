# 逻辑文件
from Serial_Port import Open_port,Close_port,Refresh_Port,Receive_information
import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import *
from Ui_SerialPort_1 import Ui_Form
import binascii
class MyMainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置实例
        self.CreateItems()
        # 设置信号与槽
        self.CreateSignalSlot()
        
    # 设置实例 
    def CreateItems(self):
        # Qt 串口类
        self.com = QSerialPort()
        # Qt 定时器类
        self.timer = QTimer(self) #初始化一个定时器
        self.timer.start(100) #设置计时间隔 100ms 并启动
        self.Init_information()
        self.Data = ''
        self.txData_1 = ''
        self.txData_2 = ''
        self.txData_3 = ''
        self.txData_4 = ''

    def Init_information(self):
        
        com = QSerialPort()
        com_list = QSerialPortInfo.availablePorts()
        for info in com_list:
            com.setPort(info)
            if com.open(QSerialPort.ReadWrite):
                self.Com_Name_Combo.addItem(info.portName())
                com.close()
        
    # 设置信号与槽
    def CreateSignalSlot(self):
        self.Com_Open_Button.clicked.connect(self.Com_Open_Button_clicked) 
        self.Com_Close_Button.clicked.connect(self.Com_Close_Button_clicked) 
        self.Send_Button.clicked.connect(self.SendButton_clicked) 
        self.Com_Refresh_Button.clicked.connect(self.Com_Refresh_Button_Clicked) 
        self.com.readyRead.connect(self.Com_Receive_Data) # 接收数据
        #self.Com_Indeed_Button.clicked.connect(self.Com_Indeed_Button_clicked)
        self.hexSending_checkBox.stateChanged.connect(self.hexShowingClicked)
        self.hexSending_checkBox.stateChanged.connect(self.hexSendingClicked)
        self.radioButton_1.toggled.connect(lambda :self.btnstate(self.radioButton_1))
        self.radioButton_2.toggled.connect(lambda : self.btnstate(self.radioButton_2))
        self.radioButton_3.toggled.connect(lambda :self.btnstate(self.radioButton_3))
        self.radioButton_4.toggled.connect(lambda : self.btnstate(self.radioButton_4))
   

    def btnstate(self,btn):
        self.textEdit_tip.clear()
        if btn.text()== "通道1":
            if btn.isChecked() == True:
                self.textEdit_tip.insertPlainText(btn.text()+" is selected")
                self.txData_1 = self.Information_process()       
        
        if btn.text() == "通道2": 
            if btn.isChecked() == True:
                self.textEdit_tip.insertPlainText(btn.text()+" is selected")
                self.txData_2 = self.Information_process()
            
        if btn.text() == "通道3":
            if btn.isChecked() == True:
                self.textEdit_tip.insertPlainText(btn.text()+" is selected")
                self.txData_3 = self.Information_process()
                
        if btn.text() == "通道4":
            if btn.isChecked() == True:
                self.textEdit_tip.insertPlainText(btn.text()+" is selected")
                self.txData_4 = self.Information_process()
        
        if len(self.txData_1) == 12:
            if len(self.txData_2) == 12:
                if len(self.txData_3) == 12:
                    if len(self.txData_4) == 12:
                        self.Data = self.txData_1 + self.txData_2 + self.txData_3 +self.txData_4
                        print(self.Data)
                        self.textEdit_Send.clear()
                        self.textEdit_Send.insertPlainText(self.Data)
                        self.txData_1 = ''
                        self.txData_2 = ''
                        self.txData_3 = ''
                        self.txData_4 = ''
    
    def Normal(self,btn):
        if(len(btn.text()) == 0):
            num = '00'
        else:    
            num = hex(int(btn.text()))[2:]
        if len(num) == 1:
            num = '0' + num
        return num    
    #信息处理    
    def Information_process(self):
        Enable = '02'
        if self.comboBox.currentText() == "工作":
            Enable = '01'
        Fre = self.Normal(self.lineEdit_Frequency)
        Wave = self.Normal(self.lineEdit_Wavelength)
        Value =self.Normal(self.lineEdit_Value)
        Break = self.Normal(self.lineEdit_Break)
        Take = self.Normal(self.lineEdit_Take)
    
        txData =  Enable + Fre + Wave + Value + Break + Take
        return txData
    #信息显示

    def Information_show(self):
        self.textEdit_Send.clear()
    #计算校验位
    def Calculate_check(self):
        txData = self.Data
        data = bytes().fromhex(txData)
        length = len(data)
        checksum = 0
        for i in range(0, length):
            checksum ^= int.from_bytes(data[i:i+1], byteorder = 'big', signed=False)
            checksum &= 0xFF # 强制截断
        checksum = hex(int(checksum))[2:]
        if len(checksum) == 1:
            checksum = '0' + checksum
        
        txData += checksum
        return txData
    # 串口发送数据
    
    def Com_Send_Data(self):
        #发送窗口显示内容
        if self.com.isOpen() == False:
            QMessageBox.critical(self, '严重错误', '串口未打开')
            return
        self.Information_show()
        #计算校验位
        txData = self.Calculate_check()
        txData = 'FD' + txData
        print(txData)
        self.textEdit_Send.insertPlainText('\n')
        self.textEdit_Send.insertPlainText(txData)
        #发送信息
        if len(txData) == 0 : 
            return
        if self.hexSending_checkBox.isChecked() == False:
            self.com.write(txData.encode('UTF-8'))
        else:
            Data = txData.replace(' ', '')
            # 如果16进制不是偶数个字符, 去掉最后一个, [ ]左闭右开
            if len(Data)%2 == 1:
                Data = Data[0:len(Data)-1]
            # 如果遇到非16进制字符
            if Data.isalnum() is False:
                QMessageBox.critical(self, '错误', '包含非十六进制数')
            try:
                hexData = binascii.a2b_hex(Data)
                print(hexData)
            except:
                QMessageBox.critical(self, '错误', '转换编码错误')
                return
            # 发送16进制数据, 发送格式如 ‘31 32 33 41 42 43’, 代表'123ABC'
            try:
                self.com.write(hexData) 
            except:
                QMessageBox.critical(self, '异常', '十六进制发送错误')
                return

    # 串口接收数据
    def Com_Receive_Data(self):
        Receive_information(self)
     
    # 串口刷新
    def Com_Refresh_Button_Clicked(self):
        Refresh_Port(self)
    
    # 16进制显示按下   
    def hexShowingClicked(self):
        if self.hexShowing_checkBox.isChecked() == True:
            # 接收区换行
            self.textEdit_Recive.insertPlainText('\n')
    
    # 16进制发送按下   
    def hexSendingClicked(self):
        if self.hexSending_checkBox.isChecked() == True:
            pass
    
    # 发送按钮按下
    def SendButton_clicked(self):
        self.Com_Send_Data()
    # 打开按钮按下
    def Com_Open_Button_clicked(self):
        #### com Open Code here ####
        Open_port(self)

    #关闭按钮
    def Com_Close_Button_clicked(self):
        Close_port(self)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
    
