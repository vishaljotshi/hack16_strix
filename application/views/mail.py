def send_email(TO, SUBJECT, TEXT):
    import smtplib

    gmail_user = 'vjotshi007@gmail.com'
    gmail_pwd =   'mmitlohegaon@636869'
    FROM = gmail_user

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
        return True
    except:
        print "failed to send mail"
        return False
#send_email(['vishal.jotshi@gslab.com'],'test 2','hey hellobitu ')