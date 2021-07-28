"""

Functionality : 
Description : 

Version : v1.0
History : 


Completed Items : 
                1. Design

Action Items :
            1, Change date format 
            2, call the bhav copy function using the required inputs
            3, Show progress bar based on the number of downloaded file status
"""

import sys,os
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtWidgets as qtw,QtCore
from BhavCopyDemo2 import Ui_BhavCopy

from PyQt5.QtWidgets import QFileDialog

# sys.path.insert(1, 'G:\\Ajith\\Others\\Ajith-self-instresed\\NSE')

from NSEDataFetch import *
import subprocess

FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')

def explore(path):
    # explorer would choke on forward slashes
    path = os.path.normpath(path)

    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])


# class myLogin(qtw.QWidget,Ui_Form):
class BhavApplication(qtw.QWidget):
    def __init__(self):
        # super().__init__(*args,**kwargs)
        qtw.QWidget.__init__(self)
        
        self.ui = Ui_BhavCopy()
        self.ui.setupUi(self)

        self.setDefaults() #function to default the values.

        # self.ui.setWindowTitle("My Window")
        # self.ui.setWindowIcon(QtGui.QIcon('NSELogo.png'))

        self.ui.browse_btn.clicked.connect(self.ChooseFile)

        self.ui.GetBhavCopy.clicked.connect(self.generate_bhav_copy)
        
        
    def setDefaults(self):
        try:
            self.ui.comp_wise_radiobtn.setChecked(True)
            self.ui.startdate_edit.setDateTime(QtCore.QDateTime.currentDateTime())
            self.ui.enddate_edit.setDateTime(QtCore.QDateTime.currentDateTime())
            self.directory  = os.getcwd()
            self.ui.pathchooser_edit.setText(self.directory)
            self.ui.progressBar.hide()
            self.progressBarMaxValue = 100
            self.ui.progressBar.setMaximum(self.progressBarMaxValue)

        except Exception as e:
            print('Error:\t while defaulting values : ',e)
            return False
        return True


    def sample(self):
        print('Sample statements heh !!')
        # qtw.QMessageBox.information(self,'Success','User successfully logged in !!')
        # qtw.QMessageBox.critical(self,'Failed','not logged in ')


    def get_choosen_bhav_type(self): # company wise / date wise
        if self.ui.comp_wise_radiobtn.isChecked()==True:
            print('company_wise')
            return 'company_wise'
        elif self.ui.date_wise_radiobtn.isChecked()==True:
            print('date_wise')
            return 'date_wise'
    # def generate_bhav_copy(self,start_date ,end_date,splits):
    # def generate_bhav_copy(self,**kwargs):
    def generate_bhav_copy(self):

        start_date = self.ui.startdate_edit.text()
        end_date = self.ui.enddate_edit.text() 
        output_directory = self.ui.pathchooser_edit.text()
        data_requirements=[self.get_choosen_bhav_type()]
        print ('start_date:',start_date)
        print ('end_date:',end_date)
        print ('output_directory:',output_directory)
        print ('data_requirements:',data_requirements)
        try:
            download_bhav_copy(start_date=start_date,end_date=end_date,output_directory= output_directory,data_requirements = data_requirements,progressBar= self.ui.progressBar)
            self.ui.progressBar.setValue(self.progressBarMaxValue)
            qtw.QMessageBox.information(self,'Success','Files downloaded Successfully !!')
            # subprocess.Popen(r'explorer /select,"'+str(output_directory)+str('"'))
            explore(output_directory)
        except Exception as e:
            print('Exception caught while downloading bhav copies :',e)
            qtw.QMessageBox.critical(self,'Failed','Please try again !\n Error : '+str(e))
        return True


    def ChooseFile(self):
        # path_to_open  = 'G:\\Ajith\\Others\\Ajith-self-instresed\\QT-Learning\\UIDesginer\\Practising'
        
        
        # how to choose files
        # choosed_file = qtw.QFileDialog.getOpenFileName(None,"getOpenFileName","./","All Files (*);;Text Files (*.txt)")

        # print('type :',type(choosed_file))
        # print('directory :',choosed_file)
        

        # choosing directories......

        self.directory = qtw.QFileDialog.getExistingDirectory(None, "getExistingDirectory", self.directory)
        self.ui.pathchooser_edit.setText(self.directory) # assigning the coosed directory/file to our text edit. 


        # print('type :',type(directory))
        # print('directory :',directory)
        # self.ui.pathchooser_edit.setText(choosed_file[0]) # assigning the coosed directory/file to our text edit. 


        
def start():
    # window = MainWindow()
    # window.show()
    # return window    

    window = BhavApplication()
    window.show()
    return window    
    
    
if __name__ =="__main__"    :
    # for general execution
    # app = qtw.QApplication([])
    # window = start()
    # sys.exit(app.exec_())

    # for exe creation
    appctxt = ApplicationContext()
    window = start()
    sys.exit(appctxt.app.exec())

