import pypyodbc    
# connection = pypyodbc.connect('Driver={SQL Server};Server=Debendra;Database=CodeX;uid=sa;pwd=123')    
# print("Enter a Unique Id")    
# Id=int(input())    
# print("Enter first Name")    
# firstname=input()  
# print("Enter last Name")    
# LastName=input()  
# print("Enter Regno")    
# RegisterNo=int(input())   
# cursor = connection.cursor()    
# SQLCommand = ("INSERT INTO tbl_employee(id,firstName, LastName, EmployeeId) VALUES (?,?,?,?)")    
# Values = [Id,firstname,LastName,RegisterNo]   
# #Processing Query    
# cursor.execute(SQLCommand,Values)     
# #Commiting any pending transaction to the database.    
# connection.commit()    
# #closing connection    
# print("Data Successfully Inserted")   
# connection.close()

def load():
connection = pypyodbc.connect('Driver={SQL Server};Server=ssci.database.windows.net;Database=ssci_stage_new;uid=fiinduser;pwd=Welcome$11nd')    
cursor = connection.cursor()    
print 'Connection success'

for i in file_lines
SQLCommand = ("INSERT INTO tbl_employee(id,firstName, LastName, EmployeeId) VALUES ()")    
Values = [Id,firstname,LastName,RegisterNo]   
#Processing Query    
cursor.execute(SQLCommand,Values)     
#Commiting any pending transaction to the database.    
connection.commit()    
#closing connection    
print("Data Successfully Inserted")   
connection.close(