from machine import Pin, time_pulse_us
import urequests
from time import sleep
import time

# Pin setup
TRIG_PIN = Pin(5, Pin.OUT)
ECHO_PIN = Pin(18, Pin.IN)
BUZZER_PIN = Pin(19, Pin.OUT)


def connect():
    import network
 
    ssid = "smartspacekk" 
    password = "smartspace09" 
 
    station = network.WLAN(network.STA_IF)
 
    if station.isconnected() == True:
        print("Already connected")
        return
 
    station.active(True)
    station.connect(ssid, password)
 
    while station.isconnected() == False:
        pass
 
    print("Connection successful")
    print(station.ifconfig())

connect()




def get_distance():
    # Send a 10us pulse to trigger
    TRIG_PIN.off()
    time.sleep_us(2)
    TRIG_PIN.on()
    time.sleep_us(10)
    TRIG_PIN.off()

    # Measure the duration of the echo pulse
    duration = time_pulse_us(ECHO_PIN, 1, 30000)  # timeout after 30ms
    
    if duration < 0:
        return -1  # timeout or error

    # Calculate distance in cm
    distance_cm = (duration / 2) / 29.1
    return distance_cm

while True:
    distance = get_distance()
    
    if distance > 0:
        print("Distance: {:.2f} cm".format(distance))
        
        if distance < 5:
            BUZZER_PIN.on()
        else:
            BUZZER_PIN.off()
    else:
        print("Error reading distance")

    time.sleep(0.2)

    h = {'content-type' : 'application/x-www-form-urlencoded'}
    form_url = 'https://docs.google.com/forms/d/e/1FAIpQLSeKT-7XwFW3nxrGBhprCks2jXZWOCj-UAm2gq1-jFEOyXSLLA/formResponse?usp=pp_url&'
    form_data = 'entry.108654085=' + str(distance)
    r = urequests.post(form_url, data=form_data, headers=h)
    r.status_code
    r.close()
    print("check google form")
    time.sleep(10)





