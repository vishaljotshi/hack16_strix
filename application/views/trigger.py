from datetime import datetime
from threading import Timer
import urllib2
import mail,json
import ConfigParser




empDetail=[]

def generateMailMessage():
    fempList=json.loads(urllib2.urlopen('http://localhost:5000/femaleStatus').read())
    mail_message="Following female employees are still in office after 8:30 pm :\n"
    for emp in fempList:
        dta=json.loads(urllib2.urlopen('http://localhost:5000/emp/'+emp).read())
        mail_message +=dta[0]+' : '+dta[1]+'\n'
        empDetail.append(dta)
    mail_message +="Please take desired action ASAP!"
    return mail_message


print  generateMailMessage()

def checkFemaleEmployees():
    global hr_email,leaving_time

    print "info ::  Timed event triggered!"
    startJob(hr_email,leaving_time)
    mail.send_email(hr_email,'default subject',generateMailMessage())

def startJob(hr_email,leaving_time):
    print hr_email
    print leaving_time
    hr=leaving_time.split(':')[0]
    mn=leaving_time.split(':')[1]

    print 'hr email : '
    print hr_email
    print 'Event for leaving time : '+leaving_time

    x=datetime.today()
    y=x.replace(day=x.day+1, hour=int(hr), minute=int(mn), second=0, microsecond=0)
    delta_t=y-x

    secs=delta_t.seconds+1
    print "event will be triggered after "+str(secs)
    t = Timer(secs, checkFemaleEmployees)
    t.start()



config = ConfigParser.ConfigParser()
config.read('configuration.cfg')

hr_email=config.get('mail','hr_email')
leaving_time=config.get('female timings','leaving_time')
#leaving_time='00:46'
print "Job scheduled!"
startJob([hr_email],leaving_time)





