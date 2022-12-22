import random

from config.base import query,current_time,update,get_hwnd,is_txt_exists

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtGui import QIcon
from MainWindow import Ui_MainWindow

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from airtest.core.win.win import *

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)

        #设置主窗口标题名称
        self.setWindowTitle("12kele.comTG营销系统V1.0免费版")
        #设置主窗口icon
        self.setWindowIcon(QIcon('t.png'))

        # #创建状态栏的小窗口
        # self.statusBar().showMessage('Ready')

        #连接telegram
        self.pushButton_9.clicked.connect(self.get_device)

        #获取设备状态并通过控制台显示出来
        self.pushButton_9.clicked.connect(self.get_device_status)

        #获取信息模板
        self.pushButton_6.clicked.connect(self.get_message_templates)

        #导入群链接
        self.pushButton_7.clicked.connect(self.get_group)

        #导入好友链接
        self.pushButton_8.clicked.connect(self.get_friends)

        #开始群发
        self.pushButton.clicked.connect(self.start_sender)

        #停止群发
        self.pushButton.clicked.connect(self.stop_sender)


    #连接一个telegram
    def get_device(self):
        try:
            if not cli_setup():
                auto_setup(__file__,devices=["Windows:///" + str(get_hwnd('Telegram')[0])])
                # 创建devices表
                update('CREATE TABLE devices(id int,name varchar(255),process_id varchar(255),status varchar(255) )')
                self.textEdit.append(current_time() + "  " + "连接telegram成功")
                hwnd = get_hwnd('Telegram')
                sql = "INSERT INTO devices (id, name, process_id, status) VALUES ('{}','{}','{}','{}')".format(
                        '1','Telegaram',str(hwnd[0]),'正在运行'
                    )
                print(sql)
                update(sql)

        except Exception as e:
            print(e)
            self.textEdit.append(current_time() + "  " + "连接telegram失败，请重试")



    #获取连接telegram状态
    def get_device_status(self):
        try:
            devices_status = query('select * from devices')
            self.row = len(devices_status) #取得记录个数，用于设置表格行数
            self.vol = len(devices_status[0]) #取得记录个数，用于设置表格列数
            self.tableWidget.setColumnCount(self.vol) #设置表格列数
            self.tableWidget.setRowCount(self.row) #设置表格行数
            self.tableWidget.setHorizontalHeaderLabels(('ID','进程名称','进程ID','进程状态')) #设置表格标题
            self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch) #水平方向填充满表格
            self.tableWidget.verticalHeader().setVisible(False)  #设置垂直表头隐藏

            #遍历数据到表格
            for i in range(self.row):
                for j in range(self.vol):
                    self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(devices_status[i][j])))

            self.textEdit.append(current_time() + "  " + "获取telegram状态成功")


        except Exception as e:
            print(e)
            self.textEdit.append(current_time() + "  " + "获取telegram状态失败，请重试")

    #获取消息模板
    def get_message_templates(self):
        try:
            #是否创建文件的逻辑
            f = is_txt_exists('信息模板.txt')
            #查看是否已经导入文件逻辑
            if self.lineEdit_6.text():
                pass
                self.textEdit.append(current_time() + "  " + "需要重新导入请清除当前路径和内容")
                content = f.readlines()
                print(content)
                new_content = []
                for i in content:
                    i = i + "     " + "由免费版12kele.com营销系统发送"
                    new_content.append(i)
                    print(new_content)
                self.textEdit.append(current_time() + "  " + "导入消息模板成功")
                return new_content
            else:
                self.download_path = QtWidgets.QFileDialog.getOpenFileNames(None,"请选择要添加的文件",'./',"Text Files(*.txt);")
                print(self.download_path[0][0])  #读取文件路径
                content = f.readlines()
                if not self.download_path[0][0].strip():
                    pass
                else:
                    self.lineEdit_6.setText(self.download_path[0][0])
                    new_content = []
                    for i in content:
                        self.textEdit_2.append(i)
                        i = i + "     " + "由免费版12kele.com营销系统发送"
                        new_content.append(i)
                        print(new_content)
                    self.textEdit.append(current_time() + "  " + "导入消息模板成功")
                    return new_content
        except Exception as e:
            print(e)
            self.textEdit.append(current_time() + "  " + "导入消息模板失败，请重试")

    #导入待群发的群
    def get_group(self):
        try:
            f = is_txt_exists('群.txt')
            if self.lineEdit_7.text():
                pass
                self.textEdit.append(current_time() + "  " + "需要重新导入请清除当前路径和内容")
                content = f.readlines()
                print(content)
                return content
            else:
                self.download_path = QtWidgets.QFileDialog.getOpenFileNames(None, "请选择要添加的文件", './',
                                                                            "Text Files(*.txt);")
                print(self.download_path[0][0])  # 读取文件路径
                content = f.readlines()
                if not self.download_path[0][0].strip():
                    pass
                else:
                    self.lineEdit_7.setText(self.download_path[0][0])
                    self.textEdit.append(current_time() + "  " + "导入群链接成功")
                    return content
        except Exception as e:
            print(e)
            self.textEdit.append(current_time() + "  " + "导入群链接失败，请重试")

    #导入待群发的好友
    def get_friends(self):
        try:
            f = is_txt_exists('好友.txt')
            if self.lineEdit_8.text():
                pass
                self.textEdit.append(current_time() + "  " + "需要重新导入请清除当前路径和内容")
                content = f.readlines()
                print(content)
                return content
            else:
                self.download_path = QtWidgets.QFileDialog.getOpenFileNames(None, "请选择要添加的文件", './',
                                                                            "Text Files(*.txt);")
                print(self.download_path[0][0])  # 读取文件路径
                content = f.readlines()
                if not self.download_path[0][0].strip():
                    pass
                else:
                    self.lineEdit_8.setText(self.download_path[0][0])
                    self.textEdit.append(current_time() + "  " + "导入好友链接成功")
                    return content
        except Exception as e:
            print(e)
            self.textEdit.append(current_time() + "  " + "导入好友失败，请重试")

    #开始群发
    def start_sender(self):
        try:
            second = int(self.lineEdit_5.text())
            message = self.get_message_templates()
            group_choice = self.radioButton.isChecked()
            friend_choice = self.radioButton_2.isChecked()
            both_choice = self.radioButton_3.isChecked()

            number = 0

            self.textEdit.append(current_time() + "  " + "火力全开，开始群发中！！！")
            self.statusbar.showMessage('12kele.comTG营销系统正在群发中')

            if group_choice:
                link = self.get_group()
                while number < 5:   #群发次数

                    if exists(Template(r"./images/search.png", record_pos=(-0.391, -0.327), resolution=(800, 621))):

                        touch(Template(r"./images/search.png", record_pos=(-0.391, -0.327), resolution=(800, 621)))
                        # 依次取值
                        text(link[number])

                        # 判断搜索是否成功
                        exists(Template(r"./images/global.png", record_pos=(-0.403, -0.276), resolution=(800, 621)))

                        time.sleep(3)

                        keyevent("{ENTER}")

                    else:
                        keyevent("{ESC}")

                        keyevent("{ESC}")
                    #给while循环增加限制
                    number = number + 1

                    #判断是否要加入群组和发送信息
                    if exists(Template(r"./images/join.png", record_pos=(0.177, 0.358), resolution=(800, 621))):

                        touch(Template(r"./images/join.png", record_pos=(0.177, 0.358), resolution=(800, 621)))

                        exists(Template(r"./images/write.png", record_pos=(-0.011, 0.361), resolution=(800, 621)))

                        touch(Template(r"./images/write.png", record_pos=(-0.011, 0.361), resolution=(800, 621)))

                        # 随机取值
                        text(message[random.randint(0, len(message)-1)])

                        keyevent("{ENTER}")

                        self.textEdit.append(current_time() + "  " + "成功发送第{}条信息".format(number))
                        self.textEdit.repaint()
                        QtCore.QCoreApplication.processEvents()


                        time.sleep(3)

                        keyevent("{ESC}")

                        keyevent("{ESC}")

                    elif exists(Template(r"./images/write.png", record_pos=(-0.011, 0.361), resolution=(800, 621))):

                        touch(Template(r"./images/write.png", record_pos=(-0.011, 0.361), resolution=(800, 621)))

                        # 随机取值
                        text(message[random.randint(0, len(message)-1)])

                        keyevent("{ENTER}")

                        self.textEdit.append(current_time() + "  " + "成功发送第{}条信息".format(number))
                        self.textEdit.repaint()
                        QtCore.QCoreApplication.processEvents()

                        time.sleep(3)

                        keyevent("{ESC}")

                        keyevent("{ESC}")
                    else:
                        time.sleep(3)

                        keyevent("{ESC}")

                        keyevent("{ESC}")

                    if number == len(link):
                        QtWidgets.QMessageBox.warning(self, "警告", "群发已结束,免费版只能发送5次")
                        QtCore.QCoreApplication.processEvents()


                    # 下一次群发间隔时间
                    time.sleep(random.randint(0,second))

            elif friend_choice:
                link = self.get_friends()
                while number < len(link):

                    if exists(Template(r"./images/search.png", record_pos=(-0.391, -0.327), resolution=(800, 621))):

                        touch(Template(r"./images/search.png", record_pos=(-0.391, -0.327), resolution=(800, 621)))
                        # 依次取值
                        text(link[number])

                        # 判断搜索是否成功
                        exists(Template(r"./images/global.png", record_pos=(-0.403, -0.276), resolution=(800, 621)))

                        time.sleep(3)

                        keyevent("{ENTER}")

                    else:
                        keyevent("{ESC}")

                        keyevent("{ESC}")
                    # 给while循环增加限制
                    number = number + 1

                    # 判断是否要加入群组和发送信息
                    if exists(Template(r"./images/join.png", record_pos=(0.177, 0.358), resolution=(800, 621))):

                        touch(Template(r"./images/join.png", record_pos=(0.177, 0.358), resolution=(800, 621)))

                        exists(Template(r"./images/write.png", record_pos=(-0.011, 0.361), resolution=(800, 621)))

                        touch(Template(r"./images/write.png", record_pos=(-0.011, 0.361), resolution=(800, 621)))

                        # 随机取值
                        text(message[random.randint(0, len(message) - 1)])

                        keyevent("{ENTER}")

                        self.textEdit.append(current_time() + "  " + "成功发送第{}条信息".format(number))
                        self.textEdit.repaint()
                        QtCore.QCoreApplication.processEvents()

                        time.sleep(3)

                        keyevent("{ESC}")

                        keyevent("{ESC}")

                    elif exists(Template(r"./images/write.png", record_pos=(-0.011, 0.361), resolution=(800, 621))):

                        touch(Template(r"./images/write.png", record_pos=(-0.011, 0.361), resolution=(800, 621)))

                        # 随机取值
                        text(message[random.randint(0, len(message) - 1)])

                        keyevent("{ENTER}")

                        self.textEdit.append(current_time() + "  " + "成功发送第{}条信息".format(number))
                        self.textEdit.repaint()
                        QtCore.QCoreApplication.processEvents()

                        time.sleep(3)

                        keyevent("{ESC}")

                        keyevent("{ESC}")
                    else:
                        time.sleep(3)

                        keyevent("{ESC}")

                        keyevent("{ESC}")

                    if number == len(link):
                        QtWidgets.QMessageBox.warning(self, "警告", "群发已结束，免费版只能发送5次")
                        QtCore.QCoreApplication.processEvents()

                    # 下一次群发间隔时间
                    time.sleep(random.randint(0, second))

            elif both_choice:
                link = self.get_friends() + self.get_group()
                random.shuffle(link)
                print(link)
                #随机打乱待发送顺序
                while number < len(link):

                    if number == len(link):
                        QtWidgets.QMessageBox.warning(self, "警告", "群发已结束,免费版只能发送5次")

                    if exists(Template(r"./images/search.png", record_pos=(-0.391, -0.327), resolution=(800, 621))):

                        touch(Template(r"./images/search.png", record_pos=(-0.391, -0.327), resolution=(800, 621)))
                        # 依次取值
                        text(link[number])

                        # 判断搜索是否成功
                        exists(Template(r"./images/global.png", record_pos=(-0.403, -0.276), resolution=(800, 621)))

                        time.sleep(3)

                        keyevent("{ENTER}")

                    else:
                        keyevent("{ESC}")

                        keyevent("{ESC}")
                    # 给while循环增加限制
                    number = number + 1

                    # 判断是否要加入群组和发送信息
                    if exists(Template(r"./images/join.png", record_pos=(0.177, 0.358), resolution=(800, 621))):

                        touch(Template(r"./images/join.png", record_pos=(0.177, 0.358), resolution=(800, 621)))

                        exists(Template(r"./images/write.png", record_pos=(-0.011, 0.361), resolution=(800, 621)))

                        touch(Template(r"./images/write.png", record_pos=(-0.011, 0.361), resolution=(800, 621)))

                        # 随机取值
                        text(message[random.randint(0, len(message) - 1)])

                        keyevent("{ENTER}")

                        self.textEdit.append(current_time() + "  " + "成功发送第{}条信息".format(number))
                        self.textEdit.repaint()
                        QtCore.QCoreApplication.processEvents()

                        time.sleep(3)

                        keyevent("{ESC}")

                        keyevent("{ESC}")

                    elif exists(Template(r"./images/write.png", record_pos=(-0.011, 0.361), resolution=(800, 621))):

                        touch(Template(r"./images/write.png", record_pos=(-0.011, 0.361), resolution=(800, 621)))

                        # 随机取值
                        text(message[random.randint(0, len(message) - 1)])

                        keyevent("{ENTER}")

                        self.textEdit.append(current_time() + "  " + "成功发送第{}条信息".format(number))
                        self.textEdit.repaint()
                        QtCore.QCoreApplication.processEvents()


                        time.sleep(3)

                        keyevent("{ESC}")

                        keyevent("{ESC}")
                    else:
                        time.sleep(3)

                        keyevent("{ESC}")

                        keyevent("{ESC}")

                    if number == len(link):
                        QtWidgets.QMessageBox.warning(self, "警告", "群发已结束，免费版只能发送5次")
                        QtCore.QCoreApplication.processEvents()


                    # 下一次群发间隔时间
                    time.sleep(random.randint(0, second))
            else:
                    QtWidgets.QMessageBox.warning(self,"警告","请选择群发选项")



        except Exception as e:
            print(e)
            self.textEdit.append(current_time() + "  " + "12kele.com发送启动失败，请重试！！！")

    #停止群发
    def stop_sender(self):
        QtWidgets.QApplication.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
