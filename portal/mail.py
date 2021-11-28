import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def assign_notif(name,rec_add,code,p):
    instance = code.split('.')
    if(p == 0):
        msg = 'Hi '+name+' This mail is from Float Moodle notifying you that you have created an assignment named /"'+instance[1]+'/" in the course '+instance[0]+' accessible with the Code: '+code
    elif(p == 1):
        msg = 'Hi '+name+' This mail is from Float Moodle notifying you that an assginment named /"'+instance[1]+'/" has been created in the course '+instance[0]+' accessible with the Code: '+code
    else:
        msg = 'Hi '+name+' This mail is from Float Moodle notifying you that an assginment named /"'+instance[1]+'/" has been created in the course '+instance[0]+' for you to attempt. Access it with the Code: '+code
    mail_content = msg
    #The mail addresses and password
    sender_address = 'bdmfloatmoodle@gmail.com'
    sender_pass = 'bdmfloatmoodle@251'
    receiver_address = rec_add
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Assignment Release in '+instance[0]   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Assignment Release Mail Sent to '+rec_add)


def announce_notif(name,rec_add,crs,announce):
    msg = 'Hi '+name+' This mail is from Float Moodle notifying you that there has been an announcement /"'+announce+'/" in the course '+crs
    mail_content = msg
    #The mail addresses and password
    sender_address = 'bdmfloatmoodle@gmail.com'
    sender_pass = 'bdmfloatmoodle@251'
    receiver_address = rec_add
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Announcement in '+crs   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Announcement Mail Sent to '+rec_add)

def submit_notif(name,rec_add,wrk,crs):
    msg = 'Hi '+name+' This mail is from Float Moodle notifying you that you have attempted the '+wrk+' assignment in the course '+crs
    mail_content = msg
    #The mail addresses and password
    sender_address = 'bdmfloatmoodle@gmail.com'
    sender_pass = 'bdmfloatmoodle@251'
    receiver_address = rec_add
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Submission for '+crs   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Submission Mail Sent to '+rec_add)

def eval_notif(name,rec_add,wrk,crs):
    msg = 'Hi '+name+' This mail is from Float Moodle notifying you that your '+wrk+' assignment in the course '+crs+' has been evaluated'
    mail_content = msg
    #The mail addresses and password
    sender_address = 'bdmfloatmoodle@gmail.com'
    sender_pass = 'bdmfloatmoodle@251'
    receiver_address = rec_add
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Submission for '+crs   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Evaluation Mail Sent to '+rec_add)

def otp_notice(name,rec_add,otp):
    msg = 'Hi '+name+' This mail is from Float Moodle regarding your request on updating profile, you OTP: '+str(otp)
    mail_content = msg
    #The mail addresses and password
    sender_address = 'bdmfloatmoodle@gmail.com'
    sender_pass = 'bdmfloatmoodle@251'
    receiver_address = rec_add
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'otp for updating profile'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    #print('otp mail sent '+rec_add)