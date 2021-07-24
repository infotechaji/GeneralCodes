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


from PyQt5 import QtWidgets as qtw
from BhavCopyDemo2 import Ui_Form

class myLogin(qtw.QWidget,Ui_Form):
    def __init__(self,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        
        self.setupUi(self)

        self.GetBhavCopy.clicked.connect(lambda: self.generate_bhav_copy(start_date = self.startdate_edit.text(), 
                                                                        end_date = self.enddate_edit.text() ,
                                                                        splits=[self.get_choosen_bhav_type()]))
        
        
    def sample(self):
        print('Sample statements heh !!')
        # qtw.QMessageBox.information(self,'Success','User successfully logged in !!')
        # qtw.QMessageBox.critical(self,'Failed','not logged in ')


    def get_choosen_bhav_type(self): # company wise / date wise
        if self.comp_wise_radiobtn.isChecked()==True:
            print('company_wise')
            return 'company_wise'
        elif self.date_wise_radiobtn.isChecked()==True:
            print('date_wise')
            return 'date_wise'
    # def generate_bhav_copy(self,start_date ,end_date,splits):
    def generate_bhav_copy(self,**kwargs):
        for i in kwargs:
            print (i,kwargs[i])
        print('generate_bhav_copy called')
        
        
    
    
if __name__ =="__main__"    :
    app = qtw.QApplication([])


    myObj = myLogin()
    myObj.show()

    app.exec_()

