from cryptography.fernet import Fernet
import sys
# from pwd_test import * 
# from ...VPN.Credentials import *
# G:\Ajith\OtherFiles\VPN\VPN.py
# G:\Ajith\OtherFiles\Encryption\Cryptography.py

# key = Fernet.generate_key() #this is your "password"
# print (key) # need to hard code this 



def Encrypt(input_text):
	KEY=b'7x70gK7sZgCbKj6Lp4jIBCtNyAPLlvQ2HRNqKZVSaiM='
	cipher_suite = Fernet(KEY)
	return cipher_suite.encrypt(input_text.encode('utf-8'))
def Decrypt(input_text):
	KEY=b'7x70gK7sZgCbKj6Lp4jIBCtNyAPLlvQ2HRNqKZVSaiM='
	cipher_suite = Fernet(KEY)
	return cipher_suite.decrypt(input_text).decode('utf-8')

# print ('decoded_text :',decoded_text.decode('utf-8'))
if __name__=="__main__":
	# input_text=str(sys.argv[1])
	# input_text='DvAji123!$123'
	# encrypted=Encrypt(input_text)
	# print ('Encrypted text:',encrypted)
	print ('PASSWORD :',PASSWORD)
	# decrypted=Decrypt(encrypted)
	# print ('Encrypted text:',decrypted)
	print (Decrypt(PASSWORD))
	
	pass