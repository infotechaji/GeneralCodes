# this code should load the UI file directly to our code....

import sys

from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDialog,QApplication,QFileDialog,QMainWindow
# from PyQt5.uic import LoadUi # this function just imports the UI file, so we don't need to have the ui codings here...  which does not make us feel good. 


class myMainWindow(QtWidget):
    def __init__(self) -> None:
        super(myMainWindow,self).__init__()
        uic.loadUi("FileChooser.ui",self) # here we are loading the ui file to our application
        self.browse.clicked.connect(self.ChooseFile)
        
    def ChooseFile(self):
        choosed_file = QFileDialog.getOpenFilename(self,'Open Directory',os.getcwd())
        self.filename.setText(choosed_file[0]) # assigning the coosed directory/file to our text edit. 
        
        
        
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    # mw = myMainWindow()
    # widgt = QStackWidget()
    widgt = myMainWindow()
    widgt.show()
    app.exec_()
    
    
    
        
    
