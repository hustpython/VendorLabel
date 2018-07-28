#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import json
reload(sys)
sys.setdefaultencoding('utf-8')
qtCreatorFile = "./mainwindow.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def find_jpg_file(path):
    path = os.path.expanduser(path)
    xml_file_list = []
    for l in os.listdir(path):
        jpgdir1 = path+'/'+l
        if os.path.isdir(jpgdir1):
            for f in os.listdir(jpgdir1):
                filename = f
                ext = os.path.splitext(f)[1]
                if ext == '.jpg':
                    xml_file_list.append(l+'/'+filename)
    return xml_file_list
            
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton_open.clicked.connect(self.openDirClick)
        self.listWidget.itemDoubleClicked.connect(self.listItemDoubleClick)
        self.pushButton_Next.clicked.connect(self.nextImageClick)
        self.pushButton_Perv.clicked.connect(self.pervImageClick)
        self.pushButton_Row.clicked.connect(self.focusRow)
        self.pushButton_Row_copy.clicked.connect(self.copy_nextImage)
        self.pushButton_Delete.clicked.connect(self.deleteImage)
        self.pushButton_Yilei.clicked.connect(self.focusYilei)
        self.lineEdit_1.textChanged.connect(self.textChanged)
        self.lineEdit_2.textChanged.connect(self.textChanged)
        self.lineEdit_3.textChanged.connect(self.textChanged)
        self.lineEdit_4.textChanged.connect(self.textChanged)
        self.lineEdit_5.textChanged.connect(self.textChanged)
        self.lineEdit_6.textChanged.connect(self.textChanged)
        self.lineEdit_7.textChanged.connect(self.textChanged)
        self.this_path = ''
        self.this_jpg = ''
    def deleteImage(self):
        deletereply = QMessageBox.question(self,u'删除提示',u'确定要删除吗？',
                                          QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
        if deletereply == QMessageBox.Yes:
           deleteimg = self.listWidget.currentItem().text()
           jpg_path = self.this_path + '/' + deleteimg
           jpg_path = str(jpg_path).decode('utf-8')
           os.remove(jpg_path)
           delete_index = int(self.listWidget.currentRow())
           self.listWidget.takeItem(delete_index)
           json_file = self.this_path + '/'+deleteimg.split(".")[0] + ".json"
           json_file = str(json_file).decode('utf-8')
           if os.path.exists(json_file):
              os.remove(json_file)
              self.this_jpg = ''
        else:
           pass
    def focusRow(self):
        self.lineEdit_1.clearFocus()
        self.comboBox_21.setFocus()
    def focusYilei(self):
        self.lineEdit_1.clearFocus()
        self.comboBox_1.setFocus()
    def textChanged(self, text):
        ledit = self.sender()
        text2 = filter(str.isdigit, str(text))
        if len(text2) > 2:
            text2 = text2[0:2]
        if str(text) != str(text2):
            ledit.setText(str(text2))

    def nextImageClick(self):
        self.lineEdit_1.setFocus()
        cur_index = int(self.listWidget.currentRow())
        cnt = self.listWidget.count()
        OccupancyColjudgeres = self.OccupancyColjudge()
        if not OccupancyColjudgeres:
            return 
        elif cur_index < (cnt - 1):
                self.listWidget.setCurrentRow(cur_index + 1)
        else:
            self.listWidget.setCurrentRow(0)
        self.listItemDoubleClick(self.listWidget.currentItem()) 
    def copy_nextImage(self):
        #self.lineEdit_1.setFocus()
        cur_index = int(self.listWidget.currentRow())
        cnt = self.listWidget.count()
        OccupancyColjudgeres = self.OccupancyColjudge()
        if not OccupancyColjudgeres:
            return 
        elif cur_index < (cnt - 1):
                self.listWidget.setCurrentRow(cur_index + 1)
        else:
            self.listWidget.setCurrentRow(0)
        self.copyitemtonext(self.listWidget.currentItem()) 
    def pervImageClick(self):
        self.lineEdit_1.setFocus()
        cur_index = int(self.listWidget.currentRow())
        cnt = self.listWidget.count()
        OccupancyColjudgeres = self.OccupancyColjudge()
        if not OccupancyColjudgeres:
            return 
        elif cur_index > 0:
            self.listWidget.setCurrentRow(cur_index - 1)
        else:
            self.listWidget.setCurrentRow(cnt - 1)
        self.listItemDoubleClick(self.listWidget.currentItem())
        
    def openDirClick(self):
        if self.this_jpg != '':
            self.saveJson(self.this_jpg)
        self.this_path = ""
        self.this_jpg = ""
        if os.path.exists('dir.txt'):
            temp_path = self.read_file('dir.txt')
        else:
            temp_path = ""
        print temp_path
        self.this_path = QtGui.QFileDialog.getExistingDirectory(self, "choose directory", temp_path)
        self.write_file('dir.txt', self.this_path)
        jpg_list = find_jpg_file(self.this_path)
        self.listWidget.clear()
        for jpg in jpg_list:
            self.listWidget.addItem(jpg)
        self.refreshListView()
    def copyitemtonext(self, item):
        #self.lineEdit_1.setFocus()
        if self.this_jpg != '':
            data = self.saveJson(self.this_jpg)
        self.this_jpg = item.text()
        self.copy_loadJson(data)
        self.refreshListView()
        jpg_path = self.this_path + '/' + self.this_jpg
        image = QtGui.QImage()
        if image.load(jpg_path):
            image = image.scaled(self.scrollAreaWidgetContents.width(), self.scrollAreaWidgetContents.height(),
                                 QtCore.Qt.KeepAspectRatioByExpanding)
            scene = QtGui.QGraphicsScene()
            scene.addPixmap(QtGui.QPixmap.fromImage(image))
            self.graphicsView.setScene(scene)
            # self.graphicsView.resize(self.scrollAreaWidgetContents.width(), self.scrollAreaWidgetContents.height())
            self.graphicsView.show()
    def listItemDoubleClick(self, item):
        self.lineEdit_1.setFocus()
        OccupancyColjudgeres = self.OccupancyColjudge()
        if not OccupancyColjudgeres:
            return
        if self.this_jpg != '':
            self.saveJson(self.this_jpg)
        self.this_jpg = item.text()
        self.loadJson(self.this_jpg)
        self.refreshListView()
        jpg_path = self.this_path + '/' + self.this_jpg
        image = QtGui.QImage()
        if image.load(jpg_path):
            image = image.scaled(self.scrollAreaWidgetContents.width(), self.scrollAreaWidgetContents.height(),
                                 QtCore.Qt.KeepAspectRatioByExpanding)
            scene = QtGui.QGraphicsScene()
            scene.addPixmap(QtGui.QPixmap.fromImage(image))
            self.graphicsView.setScene(scene)
            # self.graphicsView.resize(self.scrollAreaWidgetContents.width(), self.scrollAreaWidgetContents.height())
            self.graphicsView.show()

    def write_file(self, file_name, content):
        f = file(file_name, "a+")
        f.truncate()
        f.write(content)
        f.close()

    def read_file(self, file_name):
        f = open(file_name)
        r = f.read()
        f.close()
        return r

    def refreshListView(self):
        c = self.listWidget.count()
        for i in range(0, c):

            jpg_name = self.listWidget.item(i).text()
            file_name = self.this_path + '/' + jpg_name.split(".")[0] + ".json"
            if os.path.exists(file_name):
                self.listWidget.item(i).setBackground(QtGui.QColor(255, 200, 0))
    def OccupancyColjudge(self):
        temp_value = []
        left_id = []
        right_id = []
        temp_value.append(self.comboBox_21.currentIndex())
        temp_value.append(self.comboBox_22.currentIndex())
        temp_value.append(self.comboBox_23.currentIndex())
        temp_value.append(self.comboBox_24.currentIndex())
        temp_value.append(self.comboBox_25.currentIndex())
        temp_value.append(self.comboBox_26.currentIndex())
        temp_value.append(self.comboBox_27.currentIndex())
        #单列：0；多列左：1；多列中：2；多列右：3；

        def comparePreNext(a,b):
            if a == 0 and b not in [0,1]:
                return False
            elif a == 1 and b not in [2,3]:
                return False
            elif a == 2 and b not in [2,3]:
                return False
            elif a == 3 and b not in [0,1]:
                return False
            return True
        def lastcoljudge():
            if temp_value[-1] in [1,2]:
                return False
            return True
        for i in xrange(len(temp_value)-1):
            pre_val = temp_value[i]
            next_val = temp_value[i+1]
            msg = u"占用列中第{}列填写错误,请检查修改！".format(i+2)
            if i == len(temp_value)-2 and not lastcoljudge():
               self.warning(msg)
               return False
            if not comparePreNext(pre_val,next_val):          
               self.warning(msg)
               return False
            if pre_val == 1 and i not in left_id:
               left_id.append(i)
            if next_val == 1 and i+1 not in left_id:
               left_id.append(i+1)
            if pre_val == 3 and i not in right_id:
               right_id.append(i)
            if next_val == 3 and i+1 not in right_id:
               right_id.append(i+1)
        if len(left_id) == len(right_id) == 0:
            return True
        if not self.countjudge(left_id,right_id):
            countmsg = u"多列左与多列右之间的商品数量不相同"
            self.warning(countmsg)
            return False
        return True
    def countjudge(self,leftid,rightid):
        count_value = []
        count_value.append(self.lineEdit_1.text().toInt()[0])
        count_value.append(self.lineEdit_2.text().toInt()[0])
        count_value.append(self.lineEdit_3.text().toInt()[0])
        count_value.append(self.lineEdit_4.text().toInt()[0])
        count_value.append(self.lineEdit_5.text().toInt()[0])
        count_value.append(self.lineEdit_6.text().toInt()[0])
        count_value.append(self.lineEdit_7.text().toInt()[0])
        count_compare = [[i for i in count_value[l:r+1]] for l,r in zip(leftid,rightid)] 
        for one_group in count_compare:
            if len(set(one_group)) != 1:
               return False
        return True
    def warning(self,msg):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(msg)
        msgBox.exec_()
    def copy_loadJson(self,pre_data):
        
        if not self.checkBox.isChecked():
            self.comboBox_21.setCurrentIndex(pre_data[1][0])
            self.comboBox_22.setCurrentIndex(pre_data[1][1])
            self.comboBox_23.setCurrentIndex(pre_data[1][2])
            self.comboBox_24.setCurrentIndex(pre_data[1][3])
            self.comboBox_25.setCurrentIndex(pre_data[1][4])
            self.comboBox_26.setCurrentIndex(pre_data[1][5])
            self.comboBox_27.setCurrentIndex(pre_data[1][6])
        self.lineEdit_1.setText(str(pre_data[3][0]))
        self.lineEdit_2.setText(str(pre_data[3][1]))
        self.lineEdit_3.setText(str(pre_data[3][2]))
        self.lineEdit_4.setText(str(pre_data[3][3]))
        self.lineEdit_5.setText(str(pre_data[3][4]))
        self.lineEdit_6.setText(str(pre_data[3][5]))
        self.lineEdit_7.setText(str(pre_data[3][6]))

    def loadJson(self, last_jpg):
        file_name = self.this_path + '/' + last_jpg.split(".")[0] + ".json"
        if os.path.exists(file_name):
            json_str = self.read_file(file_name)
            data = json.loads(json_str)
            for i in range(1, 4):
                item = data[i]
                if i == 1:
                    self.comboBox_21.setCurrentIndex(item[0])
                    self.comboBox_22.setCurrentIndex(item[1])
                    self.comboBox_23.setCurrentIndex(item[2])
                    self.comboBox_24.setCurrentIndex(item[3])
                    self.comboBox_25.setCurrentIndex(item[4])
                    self.comboBox_26.setCurrentIndex(item[5])
                    self.comboBox_27.setCurrentIndex(item[6])
                elif i == 2:
                    self.comboBox_1.setCurrentIndex(item[0])
                    self.comboBox_2.setCurrentIndex(item[1])
                    self.comboBox_3.setCurrentIndex(item[2])
                    self.comboBox_4.setCurrentIndex(item[3])
                    self.comboBox_5.setCurrentIndex(item[4])
                    self.comboBox_6.setCurrentIndex(item[5])
                    self.comboBox_7.setCurrentIndex(item[6])
                elif i == 3:
                    self.lineEdit_1.setText(str(item[0]))
                    self.lineEdit_2.setText(str(item[1]))
                    self.lineEdit_3.setText(str(item[2]))
                    self.lineEdit_4.setText(str(item[3]))
                    self.lineEdit_5.setText(str(item[4]))
                    self.lineEdit_6.setText(str(item[5]))
                    self.lineEdit_7.setText(str(item[6]))
        else:
            if not self.checkBox.isChecked():
                self.comboBox_21.setCurrentIndex(0)
                self.comboBox_22.setCurrentIndex(0)
                self.comboBox_23.setCurrentIndex(0)
                self.comboBox_24.setCurrentIndex(0)
                self.comboBox_25.setCurrentIndex(0)
                self.comboBox_26.setCurrentIndex(0)
                self.comboBox_27.setCurrentIndex(0)
            self.comboBox_1.setCurrentIndex(0)
            self.comboBox_2.setCurrentIndex(0)
            self.comboBox_3.setCurrentIndex(0)
            self.comboBox_4.setCurrentIndex(0)
            self.comboBox_5.setCurrentIndex(0)
            self.comboBox_6.setCurrentIndex(0)
            self.comboBox_7.setCurrentIndex(0)
            self.lineEdit_1.setText('0')
            self.lineEdit_2.setText('0')
            self.lineEdit_3.setText('0')
            self.lineEdit_4.setText('0')
            self.lineEdit_5.setText('0')
            self.lineEdit_6.setText('0')
            self.lineEdit_7.setText('0')
   
    def saveJson(self, last_jpg):
        if last_jpg != '':
            data = [[1, 2, 3, 4, 5, 6, 7]]
            data.append(
                [
                    self.comboBox_21.currentIndex(),
                    self.comboBox_22.currentIndex(),
                    self.comboBox_23.currentIndex(),
                    self.comboBox_24.currentIndex(),
                    self.comboBox_25.currentIndex(),
                    self.comboBox_26.currentIndex(),
                    self.comboBox_27.currentIndex(),
                ]
            )
            data.append(
                [
                    self.comboBox_1.currentIndex(),
                    self.comboBox_2.currentIndex(),
                    self.comboBox_3.currentIndex(),
                    self.comboBox_4.currentIndex(),
                    self.comboBox_5.currentIndex(),
                    self.comboBox_6.currentIndex(),
                    self.comboBox_7.currentIndex(),
                ]
            )

            data.append(
                [
                    self.lineEdit_1.text().toInt()[0],
                    self.lineEdit_2.text().toInt()[0],
                    self.lineEdit_3.text().toInt()[0],
                    self.lineEdit_4.text().toInt()[0],
                    self.lineEdit_5.text().toInt()[0],
                    self.lineEdit_6.text().toInt()[0],
                    self.lineEdit_7.text().toInt()[0],
                ]
            )
            json_str = json.dumps(data)
            file_name = self.this_path + '/' + self.this_jpg.split(".")[0] + ".json"
            self.write_file(file_name, json_str)
        return data


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
