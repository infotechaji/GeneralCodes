# from PyQt5.QtWidgets import Application


from PyQt5 import QtWidgets as qtw
from UserPwd import Ui_LoginForm

# from PyQt5 import uic
# uic.loadUi('UserPwd.ui',self)


# class myLogin(qtw.QWidget):
#     def __init__(self,*args,**kwargs) -> None:
#         super().__init__(*args,**kwargs)
#         self.ui = Ui_Form()
#         self.ui.setupUi(self)
        
#         self.ui.login_button.clicked.connect(lambda:self.do_login())
#     def sample(self):
#         print('Sample statements heh !!')
    
#     def do_login(self):
#         print (self.ui.user_edit.text())
#         print (self.ui.password_edit.text())
#         if self.ui.user_edit.text() == 'user' and self.ui.password_edit.text() == 'pass':
#             print ('login success')
#             qtw.QMessageBox.information(self,'Success','User successfully logged in !!')
            
#         else:
#             print ('login failed')
#             qtw.QMessageBox.critical(self,'Failed','not logged in ')


class myLogin(qtw.QWidget,Ui_LoginForm):
    def __init__(self,*args,**kwargs) -> None:
        super().__init__(*args,**kwargs)
        
        self.setupUi(self)
        
        self.login_button.clicked.connect(lambda:self.do_login())
    def sample(self):
        print('Sample statements heh !!')
    
    def do_login(self):
        print (self.user_edit.text())
        print (self.password_edit.text())
        if self.user_edit.text() == 'user' and self.password_edit.text() == 'pass':
            print ('login success')
            qtw.QMessageBox.information(self,'Success','User successfully logged in !!')
            
        else:
            print ('login failed')
            qtw.QMessageBox.critical(self,'Failed','not logged in ')
        
        
    
    
    
app = qtw.QApplication([])


myObj = myLogin()
myObj.show()

app.exec_()

