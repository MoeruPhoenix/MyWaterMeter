from time import sleep
import RPi.GPIO as GPIO
import MySQLdb
import time

from datetime import datetime
from decimal import Decimal

from datetime import datetime

def watersensor():
    try:
        GPIO.setmode(GPIO.BOARD)

        PIN_TRIGGER = 7
        PIN_ECHO = 11

        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        #print("Waiting for sensor to settle")

        time.sleep(2)

        #print("Calculating distance")

        GPIO.output(PIN_TRIGGER, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO) == 0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO) == 1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        print("Distance:", distance, "cm")
        time.sleep(5)

    finally:
        GPIO.cleanup()
        sensorValue = distance
        print(sensorValue)
        
        return sensorValue


print('Start')
while (True):
    hostname = 'localhost'
    username = 'root'
    password = '123'
    database = 'wmdata'
        
    myConnection = MySQLdb.connect ( host=hostname, user=username, passwd=password, db=database)
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y | %H:%M:%S")   
    reading = str(watersensor())
    cur = myConnection.cursor()
    cur.execute ("INSERT INTO waterLevel (water_level, timestamp) VALUES (%s, %s)", (reading, date_time))
    myConnection.commit ()
    print (str(reading) + "sent to db")
    print("")
    print("")
    cur.close()
    myConnection.close()
    time.sleep(5)

