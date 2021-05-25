from time import sleep
import RPi.GPIO as GPIO
import MySQLdb
import time
import io
import sys
import fcntl
import copy
import string
from AtlasI2C import (
	 AtlasI2C
)

from datetime import datetime
from decimal import Decimal

from datetime import datetime

def get_devices():
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []
    
    for i in device_address_list:
        device.set_i2c_address(i)
        response = device.query("I")
        moduletype = response.split(",")[0] 
        response = device.query("name,?").split(",")[0]
        device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
    return device_list

def phsensor():
    device_list = get_devices()
        
    device = device_list[0]
    reading = ""
    x=0
    
    while x == 0:
            try:
                user_cmd = "i"
                cmd_list = "i"
                if(len(cmd_list) > 1):
                    addr = cmd_list[0]
                    
                    # go through the devices to figure out if its available
                    # and swith to it if it is
                    switched = False
                    for i in device_list:
                        if(i.address == int(addr)):
                            device = i
                            switched = True
                    if(switched):
                        print(device.query(cmd_list[1]))
                        
                    else:
                        print("No device found at address " + addr)
                else:
                    # if no address change, just send the command to the device
                    reading = (device.query(user_cmd))
            except IOError:
                print("Query failed \n - Address may be invalid, use list command to see available addresses")
            
            x = x+1
    inReading = float(reading) + 5.14
    reading = str(inReading)
    return reading


def watersensor():
    try:
        GPIO.setmode(GPIO.BOARD)

        PIN_TRIGGER = 7
        PIN_ECHO = 11

        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        time.sleep(2)

        GPIO.output(PIN_TRIGGER, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO) == 0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO) == 1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print("Distance:", distance, "cm")

    finally:
        GPIO.cleanup()
        sensorValue = distance
        
        return sensorValue
    

device_list = get_devices()
device = device_list[0]

print('Start')
while (True):
    hostname = 'localhost'
    username = 'root'
    password = '123'
    database = 'wmdata'
        
    myConnection = MySQLdb.connect ( host=hostname, user=username, passwd=password, db=database)
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y | %H:%M:%S")   
    waterReading = str(watersensor())
    pH_Reading = str(phsensor())
    
    print("pH Level: " + pH_Reading + "\n")
    
    cur = myConnection.cursor()
    cur.execute ("INSERT INTO waterLevel (water_level, timestamp) VALUES (%s, %s)", (waterReading, date_time))
    cur.execute ("INSERT INTO phlevel (ph_level, ph_timestamp) VALUES (%s, %s)", (pH_Reading, date_time))
    myConnection.commit ()
    print (str(waterReading) + " Water level sent to database")
    print (str(pH_Reading) + " pH level sent to database")
    print("")
    print("")
    cur.close()
    myConnection.close()
    time.sleep(5)