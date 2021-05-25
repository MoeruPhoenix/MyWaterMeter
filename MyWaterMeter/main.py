from flask import Flask, render_template, redirect, url_for, request, flash
from flaskext.mysql import MySQL
from datetime import datetime
from decimal import Decimal

from datetime import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
mysql = MySQL()
mysql.init_app(app)
 
import re

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config ['MYSQL_DATABASE_PASSWORD'] = '123'
app.config ['MYSQL_DATABASE_DB'] = 'wmdata' 



@app.route('/')
def index():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT water_level FROM waterLevel ORDER BY rID DESC LIMIT 1") 
    reading = cur.fetchall()
    reading = str(reading)
    reading = re.sub("\D", "", reading)
    #reading = Decimal(reading)
    
    cur.close()
    
    curpH = mysql.get_db().cursor()
    curpH.execute("SELECT ph_level from phlevel ORDER BY pHID DESC LIMIT 1")
    phreading = curpH.fetchall()
    phreading = str(phreading)
    phreading = phreading[3] + phreading[4]
    phreading = re.sub("\D", "", phreading)
    curpH.close()
    
    
    curRem = mysql.get_db().cursor()
    res = curRem.execute ("SELECT * FROM reminderTbl")
    rem = curRem.fetchall()
    curRem.close()
    
    curCheck = mysql.get_db().cursor()
    curCheck.execute("SELECT WaterLevel from reminderTbl")
    amount = curCheck.execute("SELECT WaterLevel from reminderTbl")
    check = curCheck.fetchall()
    curRem.close()
    
    count = 0
    
    if amount != 0:
        for x in check:
            checker = str(check[count])
            checker = re.sub("\D", "", checker)
            checker = int(checker)
            count = count + 1
            
            print(checker, " ya", reading)
            if checker > int(reading):
                flash("Reminder Triggered! Check Reminders Section.")
        
    count = 0
             
    print(amount)
     
    curTs = mysql.get_db().cursor()
    curTs.execute("SELECT timestamp FROM waterLevel ORDER BY rID DESC LIMIT 1")
    ts = curTs.fetchall()
    
    now = datetime.now()
    time = now.strftime("%H:%M:%S") 
    curTs.close() 
    tsa = ts[0] 
    
    return render_template('index.html', result=reading, pHresult=phreading, timeresult=time, amm=rem)

@app.route('/about') 
def about():
    return render_template('AboutUs.html') 

@app.route('/contact')
def contact():
    return render_template('ContactUs.html')

@app.route('/faq')
def faq():
    return render_template('FAQ.html')

@app.route('/sitemap')
def sitemap():
    return render_template('SiteMap.html')


@app.route('/addReminder', methods=['GET', 'POST'])
def addReminder():
    if request.method == 'POST':
        Water_level= int(request.form['wlevel'])
        descrip = request.form['descrp']
        
        connection = mysql.get_db()
        curRem = mysql.get_db().cursor()
        curRem.execute("INSERT INTO reminderTbl (Description, WaterLevel) VALUES (%s, %s)", (descrip, Water_level))
        connection.commit()
        #flash("Reminder Successfully Added!")
        curRem.close()
        return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    connection = mysql.get_db()
    curD = mysql.get_db().cursor()
    curD.execute("DELETE FROM reminderTbl WHERE SN=%s", (id,))
    connection.commit()
    curD.close()
    #flash("Reminder Successfully Deleted!")
    
    return redirect(url_for('index'))
    
if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0') 