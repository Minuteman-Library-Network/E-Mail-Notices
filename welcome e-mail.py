#!/usr/bin/env python3

"""Produces and sends welcome e-mails to newly registered patrons

Author: Jeremy Goldstein, based in part on code provided by Gem Stone-Logan
Contact Info: jgoldstein@minlib.net
"""

import psycopg2
import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from datetime import date

#use file to gather stats for how many messages are generated each day
csvFile = 'Stats\\New_Patrons.csv'

# These are variables for the email that will be sent.
# Make sure to use your own library's email server (emaihost)
#
emailhost = ''
emailuser = ''
emailpass = ''
emailport = ''


# Enter your own email information
emailfrom= ''


#Connecting to Sierra PostgreSQL database

#Enter your username, password and host

conn = psycopg2.connect("dbname='iii' user='' host='' port='1032' password='' sslmode='require'")

#Opening a session and querying the database for weekly new items
cursor = conn.cursor()
cursor.execute(open("welcome e-mail.sql","r").read())
#For now, just storing the data in a variable. We'll use it later.
rows = cursor.fetchall()
conn.close()

#Track # of generated messages count
with open(csvFile, 'a') as tempFile:
    newRow = '\n' + str(len(rows)) + ',' + str(date.today())
    tempFile.write(newRow)
tempFile.close()


for rownum, row in enumerate(rows):
    #Sending the email message
    smtp = smtplib.SMTP(emailhost, emailport)
    #for Google connection
    smtp.ehlo()
    smtp.starttls()
    smtp.login(emailuser, emailpass)
    	
    # emailto can send to multiple addresses by separating emails with commas
    emailto = [str(row[2])]	
    emailsubject = 'Enjoy your new library card!'
    #Creating the email message
    
    #plain text version
    text = '''Dear {} {},    
    Welcome! You have been registered for a library card from {}.
    
    With your new library card you can:
    
    -Borrow and request items from all Minuteman member libraries.  Most materials can be returned at any Minuteman location.
    -Visit the shared catalog at find.minlib.net  to discover books, movies, music, audiobooks, and much more.
    -Access digital ebooks, audiobooks, and streaming video from OverDrive.
    -Renew items, pay fines online, and track your reading history with MyAccount. To get started, go to find.minlib.net/iii/encore/myaccount and follow the instructions to set-up your login.
    -You can also save time by adding the Minuteman App and Text Message Notifications to your mobile phone or tablet.
    -Explore Minuteman libraries’ ever-expanding collections of toys and games, telescopes, household tools, musical instruments, and more. 
    
    '''.format(str(row[0]),str(row[1]),str(row[5]))
    if str(row[4]) != 'the Minuteman Library Network':
        text += ''' 
	    Visit your home library's website ({}) or talk to your librarian to find out about even more online collections, services, and events offered by your local library.<br><br>
        
        '''.format(str(row[6]))
    text += '''Enjoy your new library card!
    
    ***This is an automated email.  Do not reply.***'''
    
    #html version
    html = '''
    <html>
    <head></head>
    <body style="background-color:#DBE6F1;">
    <table style="width: 70%; margin-left: 15%; margin-right: 15%; border: 0; cellspacing: 0; cellpadding: 0; background-color: #FFFFFF;">
    <tr>
    <font face="Scala Sans, Calibri, Arial"; size="3">
    <p>Dear {} {},<br><br>    
    Welcome! You have been registered for a library card from <a href="{}">{}.<br><br>
        
    With your new library card you can:<br><br>
    <ul>
    <li>Borrow and request items from all <a href="http://www.mln.lib.ma.us">Minuteman member libraries</a>.  Most materials can be returned at any Minuteman location.</li>
    <li>Visit the shared catalog at <a href="http://find.minlib.net">find.minlib.net</a> to discover books, movies, music, audiobooks, and much more.</li>
    <li>Access digital ebooks, audiobooks, and streaming video from <a href="minuteman.overdrive.com">OverDrive.</a></li>
    <li>Renew items, pay fines online, and track your reading history with MyAccount.  To get started, go to <a href="http://find.minlib.net/iii/encore/myaccount">find.minlib.net/iii/encore/myaccount</a> and follow the instructions to set-up your login.</li>
    <li>You can also save time by adding the <a href="http://www.mln.lib.ma.us/catalog/faq_app.htm">Minuteman App</a> and <a href="http://www.mln.lib.ma.us/shoutbomb.htm">Text Message Notifications</a> to your mobile phone or tablet.</li>
    <li>Explore Minuteman libraries’ ever-expanding collections of toys and games, telescopes, household tools, musical instruments, and more.</li>
    </ul><br>
    '''.format(str(row[0]),str(row[1]),str(row[6]),str(row[5]))
    if str(row[4]) != 'the Minuteman Library Network':
        html += ''' 
	    Visit <a href="{}">your home library’s website</a> or talk to your librarian to find out about even more online collections, services, and events offered by your local library.<br><br>
        '''.format(str(row[6]))
    html += '''Enjoy your new library card!
    ***This is an automated email.  Do not reply.***<br><br>
    </font>
    </p>
    <img src="http://www.mln.lib.ma.us/graphics/logo-print-small.jpg" alt="Minuteman logo" height="32" width="188">
    </tr>
    </table>
    </body>  
    </html>
    '''
    
    msg = MIMEMultipart('alternative')
    part1 = MIMEText(text,'plain')
    part2 = MIMEText(html, 'html')
    msg['From'] = emailfrom
    if type(emailto) is list:
        msg['To'] = ', '.join(emailto)
    else:
        msg['To'] = emailto
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = emailsubject
    msg.attach (part1)
    msg.attach (part2)
       
    smtp.sendmail(emailfrom, emailto, msg.as_string())
    rownum+1 
    
    smtp.quit()
    
  
