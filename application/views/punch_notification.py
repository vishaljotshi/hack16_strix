from application import app
from application import mysql
from flask import send_from_directory,jsonify,render_template
import json,ConfigParser

@app.route("/")
def welcome():
    return send_from_directory("templates","index.html")


@app.route('/static/<name>')
def sendStaticResource(name):
    return send_from_directory('static',name)

@app.route("/status")
def Authenticate():
    cursor = mysql.connect().cursor()
    cursor.execute("select count(*) as count,employee_data.id,gender,punch_event from employee_data,punch_application where employee_data.id=punch_application.id group by employee_data.id,punch_event")
    data = cursor.fetchall()
    if data is None:
     return "Username or Password is wrong"
    else:
        outputObj=(makeDict(data))
        totalIn,fem=calculateInCount(outputObj)
        return json.dumps(totalIn)

@app.route("/status/floor/<numb>")
def getStatusByFloor(numb):
    cursor = mysql.connect().cursor()
    cursor.execute("select count(*) as count,employee_data.id,gender,punch_event from employee_data,punch_application where punch_application.floor='"+numb+"' and  employee_data.id=punch_application.id group by employee_data.id,punch_event")
    data = cursor.fetchall()
    if data is None:
     return "Username or Password is wrong"
    else:
        outputObj=(makeDict(data))
        totalIn,fem=calculateInCount(outputObj)
        return json.dumps(totalIn)

@app.route("/femaleStatus")
def femaleEmpStatus():
    cursor = mysql.connect().cursor()
    cursor.execute("select count(*) as count,employee_data.id,gender,punch_event from employee_data,punch_application where employee_data.gender='Female' and employee_data.id=punch_application.id group by employee_data.id,punch_event")
    data = cursor.fetchall()
    if data is None:
     return "Username or Password is wrong"
    else:
        outputObj=(makeDict(data))
        totalIn,fem=calculateInCount(outputObj)
        return json.dumps(fem)

@app.route("/emp/<id>")
def getEmpById(id):
    cursor = mysql.connect().cursor()
    cursor.execute("select * from employee_data where id="+id)
    data = cursor.fetchall()
    if data is None:
        return "Username or Password is wrong"
    else:
        try:
            return json.dumps(data[0])
        except:
            return "Employee not found!!"

@app.route("/interval")
def getIntervalData():
    cursor = mysql.connect().cursor()
    cursor.execute("select hour(punch_time) time_hour,count(id) punches from punch_application group by hour(punch_time) order by time_hour asc")
    data = cursor.fetchall()
    if data is None:
        return "No data"
    else:
        try:
            return json.dumps(data)
        except:
            return "no data"

@app.route("/restriction")
def showRestrictions():
    config = ConfigParser.ConfigParser()
    config.read('configuration.cfg')
    hr_email=config.get('mail','hr_email')
    leaving_time=config.get('female timings','leaving_time')
    return '{ "hr_email": "'+hr_email+'","leaving_time":"'+leaving_time+'"} '




def makeDict(l):
    k={}
    for val in l:
        if val[1] not in k:
            k[val[1]]={'in':'','out':''}
        if val[3]=='in':
                k[val[1]]['in']=val[0]

        elif val[3]=='out':
                k[val[1]]['out']=val[0]

    return k

def calculateInCount(data):
    femaleEmp=[]
    totalIn=0
    for f,v in data.iteritems():
        if(v['in']>v['out']) or v['out']=='':
            totalIn +=1 #employee is inside
            femaleEmp.append(f)
            print femaleEmp
    return totalIn,femaleEmp
