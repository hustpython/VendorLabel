#!/usr/bin/python
# -*- coding: utf-8 -*-
#==========================导入内置库=================
import os
import sys
import shutil
#from os import symlink
__CSL = None
def symlink(source, link_name):
    '''symlink(source, link_name)
       Creates a symbolic link pointing to source named link_name'''
    global __CSL
    if __CSL is None:
        import ctypes
        csl = ctypes.windll.kernel32.CreateSymbolicLinkW
        csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
        csl.restype = ctypes.c_ubyte
        __CSL = csl
    flags = 0
    if source is not None and os.path.isdir(source):
        flags = 1
    if __CSL(link_name, source, flags) == 0:
        raise ctypes.WinError()

os.symlink = symlink

import json
#=====================导入与PyQt相关的库和文件===========
from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = "./labelcheck.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

def main(two_path):
    #reload(sys)
    #sys.setdefaultencoding('utf-8')
    current_path = os.getcwd()
    current_file_path_x = str(two_path[0]).decode('utf-8')
    current_file_path_y = str(two_path[1]).decode('utf-8')
    target_path = os.path.join(current_path, 'wrong')
    # 如果存在则删除再创建目录

    if os.path.exists(target_path):
        shutil.rmtree(target_path)

    os.makedirs(target_path)

    x_dict = check_all_json(current_file_path_x)
    y_dict = check_all_json(current_file_path_y)
    more_dict = dict(x_dict,**y_dict)
    aaaa = 0
    deleteindex = 0
    for (key, value) in more_dict.items():
            x_flag = 0
            y_flag = 0
            x_json = 'a'
            y_json = 'b'
            if key in y_dict.keys():
                y_image_file = os.path.join(current_file_path_y, y_dict[key])
                y_json_file_json = y_image_file[:-3] + 'json'
                y_json = read_json_python2(y_json_file_json)
                y_flag = 1
            if key in x_dict.keys():
                x_image_file = os.path.join(current_file_path_x, x_dict[key])
                x_json_file_json = x_image_file[:-3] + 'json'
                x_json = read_json_python2(x_json_file_json)
                x_flag = 1
            
            if x_json == y_json:
                continue
            if  x_flag == 1 and y_flag != 1 :
                os.remove(x_image_file)
                if os.path.exists(x_json_file_json):
                    os.remove(x_json_file_json)
                deleteindex += 1
            if  y_flag ==1 and x_flag != 1 :
                os.remove(y_image_file)
                if os.path.exists(y_json_file_json):
                    os.remove(y_json_file_json)
                deleteindex += 1
            if x_flag and y_flag:
                new_target_path = os.path.join(target_path, str(aaaa))
                os.makedirs(new_target_path)
                aaaa += 1
                new_image_x_path = os.path.join(new_target_path, str(x_dict[key][:-4] + '_x'+str(aaaa) + '.jpg').split('/')[-1])
                new_json_x_path = os.path.join(new_target_path, str(x_dict[key][:-4] + '_x' +str(aaaa)+ '.json').split('/')[-1])    
                symlink(x_image_file, new_image_x_path)
                symlink(x_json_file_json, new_json_x_path)
            
                new_image_y_path = os.path.join(new_target_path, str(y_dict[key][:-4] + '_y' +str(aaaa)+ '.jpg').split('/')[-1])
                new_json_y_path = os.path.join(new_target_path, str(y_dict[key][:-4] + '_y' +str(aaaa)+ '.json').split('/')[-1])
                symlink(y_image_file, new_image_y_path)
                symlink(y_json_file_json, new_json_y_path)
    print("total {} wrong data,delete {} data !".format(aaaa,deleteindex))



def read_json(json_file):
    f = open(json_file, encoding='utf-8')

    r = f.read()
    f.close()

    setting = json.loads(r)

    return setting
def read_json_python2(json_file):

    f = open(json_file)
    setting = json.load(f)        #读取
    return setting

def check_all_json(current_file_path):
    x_1_10 = []

    pathDir = os.listdir(current_file_path+'/')
    for j in pathDir:
        if os.path.isdir(current_file_path+'/'+j):
            x_1_10.append(current_file_path+'/'+j)
    all_pics = []
    all_image_dir = {}
    for j in range(len(x_1_10)):
        pathpic = os.listdir(x_1_10[j])
        for _ in pathpic:
            aa = (x_1_10[j].split('/')[-1] +'/' + _).decode('utf-8')
            if _[-3:] == 'jpg' and os.path.exists(x_1_10[j]+'/'+ _[:-3]+'json'):
               all_image_dir[aa] = aa
               continue
            elif _[-4:] == 'json' and _[:-4]+'jpg' not in pathpic:
                #print('jj')
                delete_path = os.path.join(current_file_path,aa)
                os.remove(delete_path)
                continue
            elif _[-3:] == 'jpg' and _[:-3]+'json' not in pathpic:
                #print('kk')
                delete_path = os.path.join(current_file_path,aa)
                os.remove(delete_path)
            
    return all_image_dir         
    
    

#========================PyQt类====================
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.two_path = []
        #==========打开文件夹的按钮建立槽函数===========
        self.pushButton_1.clicked.connect(self.openDirClick)
        self.pushButton_2.clicked.connect(self.openDirClick)
        #=======================开始按钮==============
        self.pushButton_3.clicked.connect(self.check)
        
    def openDirClick(self):
        if len(self.two_path) == 2:
            self.two_path=[]
        self.this_path = QtGui.QFileDialog.getExistingDirectory(self, "choose directory")
        print(u"选择了文件 {}".format(str(self.this_path)))
        self.two_path.append(self.this_path)   
    
    def check(self):
        main(self.two_path)


if __name__ == '__main__':
    # if len(sys.argv) < 3:
    #     print("请增加图像数据根目录参数，例： *.py ~/source/path/ ~/target/path/")
    #     sys.exit()
    # else:
    #     main(sys.argv[1], sys.argv[2])
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.setWindowTitle(u"标签检查软件")
    window.show()
    sys.exit(app.exec_())

