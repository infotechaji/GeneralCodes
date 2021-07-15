from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
import sys

class BhavCopy(QMainWindow):
    def __init__(self):
        super(BhavCopy,self).__init__() # here we are initializing our class to the parent class
        self.setGeometry(200,200,400,400) # xpos,ypos,width.height
        self.setWindowTitle("Ajith Bhav copy app") 
        self.callUI()
        self.button_clicked =0 
    
    def callUI(self):
        x = 25
        y = 25
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("Choose start date")
        self.label1.move(x,y)
        
        
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("Choose end date")
        self.label1.move(x,y+25)
            
        
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText('GetBhavCopy')
        self.b1.move(x+50,y+50)
        self.b1.clicked.connect(self.button_fun)    


    def button_fun(self):
        # print('Button 1 is clicked')    
        self.button_clicked+=1
        self.label1.setText('You have pressed the button : '+str(self.button_clicked)+' times')
        self.update()
        
    def update(self): # size adjusts to input text.
        self.label1.adjustSize() 
    
    

def window():
    app = QApplication(sys.argv)
    win = BhavCopy()
    
    # we just named the application 

    # label1 = QtWidgets.QLabel(win)
    # label1.setText("Choose your date")
    # label1.move(25,25)

    # b1 = QtWidgets.QPushButton(win)
    # b1.setText('GetBhavCopy')
    # b1.move(50,50)
    # b1.clicked.connect(button_fun)    




    win.show()
    sys.exit(app.exec_())

window()




