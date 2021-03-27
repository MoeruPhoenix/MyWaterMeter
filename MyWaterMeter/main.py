from flask import Flask, render_template, redirect, url_for
from flaskext.mysql import MySQL
from datetime import datetime
from decimal import Decimal

from datetime import datetime

app = Flask(__name__)
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
     
    curTs = mysql.get_db().cursor()
    curTs.execute("SELECT timestamp FROM waterLevel ORDER BY rID DESC LIMIT 1")
    ts = curTs.fetchall()
    
    now = datetime.now()
    time = now.strftime("%H:%M:%S") 
    curTs.close()
    print (ts)
    tsa = ts[0]
    
    #tsa = tsa.strftime('%Y-%m-%d::%H-%M')
    print(tsa)
    
    print(reading)
        
    return render_template('index.html', result=reading, pHresult=phreading, timeresult=time)

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

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0') 