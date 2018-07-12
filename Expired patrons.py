#!/usr/bin/env python3

"""Produces and sends expiration warning e-mails to patrons whose cards expired yesterday

Author: Jeremy Goldstein, based in part on code provided by Gem Stone-Logan
Contact Info: jgoldstein@minlib.net
"""

import psycopg2
import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate
from email import encoders
from datetime import date
from dateutil.relativedelta import relativedelta

#use file to gather stats for how many messages are generated each day
#compare numbers with Expiring_Patrons.csv to see how many patrons renewed in the 30 day window
csvFile = 'Stats\Expired_Patrons.csv'

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
cursor.execute(open("Expired patrons.sql","r").read())
#For now, just storing the data in a variable. We'll use it later.
rows = cursor.fetchall()
conn.close()

#Track # of generated messages count
with open(csvFile, 'a') as tempFile:
    newRow = '\n' + str(len(rows)) + ',' + str(date.today() - relativedelta(days=1))
    tempFile.write(newRow)
tempFile.close()

#Sending the email message
smtp = smtplib.SMTP(emailhost, emailport)
#for Google connection
smtp.ehlo()
smtp.starttls()
smtp.login(emailuser, emailpass)

for rownum, row in enumerate(rows):
	
    # emailto can send to multiple addresses by separating emails with commas
    emailto = [str(row[2])]	
    emailsubject = "Your library card has expired"
    #Creating the email message
    
    #Plain text version
    text = '''Dear {} {},
     
    Your library card expired on {}.  Visit any Minuteman library for information on how to renew your account and regain access to over 6 million items.
    
    ***This is an automated email***'''.format(str(row[0]),str(row[1]),str(row[3]))
    
    #HTML version
    html = '''
    <html>
    <head></head>
    <body style="background-color:#DBE6F1;">
    <table style="width: 70%; margin-left: 15%; margin-right: 15%; border: 0; cellspacing: 0; cellpadding: 0; background-color: #FFFFFF;">
    <tr>
    <img src="cid:image1" style="height: 135px; width: 135px; display: block; margin-left: auto; margin-right: auto;" alt="placeholder">
    <font face="Scala Sans, Calibri, Arial"; size="3">
    <p>Dear {} {},<br><br>
    
    Your library card expired on {}.<br>
    Visit any <a href="http://www.mln.lib.ma.us/info/">Minuteman library</a> for information on how to renew your account and regain access to over 6 million items.<br><br>
    ***This is an automated email.  Do not reply.***<br><br>
    </font>
    </p>
    <img src="http://www.mln.lib.ma.us/graphics/logo-print-small.jpg" style="height: 32px; width: 188px; display: block; margin-left: auto; margin-right: auto;" alt="Minuteman logo">
    </tr>
    </table>
    </body>  
    </html>'''.format(str(row[0]),str(row[1]),str(row[3]))
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
    pic = open('clock.png', 'rb')
    msgImage = MIMEImage(pic.read())
    pic.close()
    
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)
    
    smtp.sendmail(emailfrom, emailto, msg.as_string())
    rownum+1
   
smtp.quit()
