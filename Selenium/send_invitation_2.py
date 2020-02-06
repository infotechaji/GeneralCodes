from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from ms_login import *

from bs4 import BeautifulSoup
#browser=webdriver.Chrome()
#browser.get('https://myinspire.microsoft.com/page/attendeenetworking?p1=eyJzcGVha2VyIjpbXSwidGltZXNsb3QiOltdLCJkYXkiOltdLCJyb29tIjpbXSwicGFnZW51bWJlciI6MSwiY2F0ZWdvcmllcyI6eyJyZWdpc3RyYW50IHRpdGxldGhhdGRlc2NyaWJlc3lvdSI6WyI1MDdkMDc0YS01ZTI4LTRiY2EtYjNkYS1kYmIyMjIyNWQ5ZjAiXSwicmVnaXN0cmFudCBhcmVhIjpbImMwMGRhZjQzLWM5MTEtNDU1Mi04NGM1LThjNDQ1MzUzMGM4ZSJdfSwia2V5d29yZCI6IiJ9')
raw_input()
ms_login('https://myinspire.microsoft.com/page/attendeenetworking?p1=eyJzcGVha2VyIjpbXSwidGltZXNsb3QiOltdLCJkYXkiOltdLCJyb29tIjpbXSwicGFnZW51bWJlciI6MSwiY2F0ZWdvcmllcyI6eyJyZWdpc3RyYW50IHRpdGxldGhhdGRlc2NyaWJlc3lvdSI6WyI1MDdkMDc0YS01ZTI4LTRiY2EtYjNkYS1kYmIyMjIyNWQ5ZjAiXSwicmVnaXN0cmFudCBhcmVhIjpbImMwMGRhZjQzLWM5MTEtNDU1Mi04NGM1LThjNDQ1MzUzMGM4ZSJdfSwia2V5d29yZCI6IiJ9')

raw_input("")
def write_subject(subject): # function for writing contents
    browser.find_element_by_name( 'messagesubject' ).send_keys(subject) # for writing message
    
def write_message(message='some messages'): # function writes the message
    browser.find_element_by_name( 'messagebody' ).send_keys(message)

def click_send(): #  function to send the message
    #browser.find_element_by_id('attendeeCatalogSendMessageButton').click()
    pass

    
def click_cancel(): # function to click cancel
    browser.find_element_by_id('attendeeCatalogMessageCloseButton').click()

for i in browser.find_elements_by_class_name('details'):

    try:
        if True:#try:
            listt = ['Katie Adams', 'Karthik Angamuthu','Kanhav Anand', 'Alaina Ankrom',  'Seung Baick', 'Ryan Baker','DeAnn Ballard','Anne Baryenbruch', 'Seanna Baumgartner', 'Lindsey Berenbach', 'Nick Blanchette', 'Fireball Brady','Colleen Bratton','Rachel Braunstein', 'Sheila Breysse', 'Rebecca Butman', 'Timothy Campbell', 'Chris Capasso', 'Melody Carlos', 'Tony Carrara', 'Tony Carrara', 'Nancy Chang', 'Marty choate', 'Luca Colicino', 'Kerry Comstock', 'Kelsey Curtis', 'Heather DeLong' , 'Stephanie Desmond', 'Heidi Eisenstein', 'Burke Fewel', 'Lindsey Frette', 'Alleah Gogley', 'Richard Hail', 'Mathieu Hannouz', 'Hailey Henry', 'Cale Hilts', 'Lauren Holland', 'Lynn Holzworth','Peter Huboi', 'Jennifer Jakubowicz', 'Matt Jennings', 'Joe Johnson', 'Lilly Keyes', 'Kirill Kotlyarenko', 'Leslie Kwoh', 'Amy Lally', 'Monica Lam', 'Erica Lien','Lindsey Lockhart','Jane Louis','Kyle McMurtry','Julianna Meidell', 'Aerin Meyers', 'Ayaka Morimoto', 'Dwight Morse', 'Nicole Munger','Tapleigh Niethamer','Rachel Parkes']
            #print len(listt)
            time.sleep(2)
            #with open("samplelep.txt","a") as fiile:
            #    fiile.write(str(i)+ "\n")
            person_name=i.find_element_by_class_name('name').text # for getting person name
            if person_name not in listt:
                i.find_element_by_class_name('message-link').click() #  For clicking MESSAGE
                print "message clicked for ",person_name
                time.sleep(1)
                write_subject('Quick catch up at MS Inspire 2017?')
                time.sleep(1)
                textt = "Hi " + person_name + ",\n\n  I was finalizing our agenda for Microsoft Inspire and noticed you are representing your company in D.C. If you have a few minutes available on Monday or Tuesday, I would like to take the opportunity to connect. \n\n If you are unfamiliar with Fiind, we are a Microsoft Managed Partner and ISV. We deliver on-demand B2B customer and market intelligence and specialize in big data, machine learning. We work with multiple Microsoft Partners and corporate teams to dramatically improve their customer intelligence and insight to drive Sales and Marketing results for Office365, Dynamics 365, Azure, SQL, and more. We integrate our solutions directly into Dynamics 365, SFDC and other CRMs as well as Marketing Automation tools such as Marketo and Eloqua. \n\n Please let me know if you have a few minutes available on the 10th or 11th as I'd very much like to meet you and learn more about your company. You can reach me at Faris@fiind.com |206.999.0767 | "
                write_message(textt)
                time.sleep(1)
                click_cancel()
                time.sleep(5)
                webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
                time.sleep(10)
    except Exception:
        # print i
        pass