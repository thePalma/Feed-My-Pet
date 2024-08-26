from bsp import board
from networking import wifi
from protocols import mqtt
from protocols import ntp
from zdm import zdm

import adc
import gpio
import serial
import time
import sg90 as servo
import oled

serial.serial()        # create a serial port with default parameters

# Variables Declaration Block
servings = 0
servings_max = 0
manual_servings = 0
auto_servings = 0
delay_servings_min = 1
ti_last_serving_min = 0

# This variables should be changed whenever we should connect to another wifi
ssid = "Iphone"                   #insert your wifi ssid here
password = "polonord"                #insert your wifi password here

# Topic where the messages will be published
sub = "IoT22_FeedMyPet"

# PIR Sensor HC-SR501 pin
pir_pin = D22                  
gpio.mode(pir_pin, INPUT)

# Buzzer pin
buzzer_pin = D25
gpio.mode(buzzer_pin, OUTPUT)

# The HCSR501 sensor requires 1 minute to initialize
print("Requires one minute to initialize")
sleep(60000)
print("Initialized")

# This function is called when a movement is detected and dispenses a serving
def movement_detected():
    global servings
    global ti_last_serving_min
    global ti_last_serving
    global auto_servings
    servo.handle_servo("open")
    servo.handle_servo("close")
    servings += 1
    auto_servings += 1
    ti_last_serving = time.localtime()
    ti_last_serving_min = ti_last_serving.to_tuple()[4]
    if (servings_max - servings) > 0:
        print_oled(ti_last_serving)
    else:
        oled.print("Replenish food!", True)
        gpio.toggle(buzzer_pin)
        sleep(500)
        gpio.toggle(buzzer_pin)
        sleep(500)
        gpio.toggle(buzzer_pin)
        sleep(500)
        gpio.toggle(buzzer_pin)
        sleep(500)
        gpio.toggle(buzzer_pin)
        sleep(500)
        gpio.toggle(buzzer_pin)
    print("Remaining servings: %d" %(servings_max - servings))
    agent.publish({"total_servings":auto_servings+manual_servings}, "servings")
    agent.publish({"auto_servings":auto_servings}, "servings")

# This function sets the number of servings to the one chosen by the user on the GUI
def change_servings(message):
    global servings_max
    global servings
    gpio.set(buzzer_pin, LOW)
    servings = 0
    servings_max = int(message)
    oled.print(("Remaining servings:"+str(servings_max)), True)

# This function is called whenever the user manually requests a serving
def manual_dispense():
    global servings_max
    global ti_last_serving
    global manual_servings
    if (servings < servings_max and servings_max != 0):
        servo.handle_servo("open")
        servo.handle_servo("close")
        servings += 1
        manual_servings += 1
        ti_last_serving = time.localtime()
        if (servings_max - servings) > 0:
            print_oled(ti_last_serving)
        else:
            oled.print("Replenish food!", True)
            gpio.toggle(buzzer_pin)
            sleep(500)
            gpio.toggle(buzzer_pin)
            sleep(500)
            gpio.toggle(buzzer_pin)
            sleep(500)
            gpio.toggle(buzzer_pin)
            sleep(500)
            gpio.toggle(buzzer_pin)
            sleep(500)
            gpio.toggle(buzzer_pin)
        print("Remaining servings: %d" %(servings_max - servings))
        agent.publish({"total_servings":auto_servings+manual_servings}, "servings")
        agent.publish({"manual_servings":manual_servings}, "servings")

# This function updates the display with the last and remaining servings
def print_oled(ti_last_serving):
    oled.print(("Last serving: " + str(ti_last_serving.tm_hour) + ":" + str(ti_last_serving.tm_min)), True)
    oled.print(("Remaining servings:"+str(servings_max-servings)), 0, 1, False)

# This is a function callable by ZDM with a job request.
# It has one parameters: the ZDM agent that receives the request.
# The function manually closes the servo if is stuck open.
def close_servo_manually(agent):
    print("Job request received!")
    servo.handle_servo("close")
    
    return("msg : Servo manually closed!")

# Callback function for handling data received from MQTT messages
def callback(client, topic, message):
    global delay_servings_min
    print("I received: ", message, " on the topic: ", topic)
    if message=="Feed":
        manual_dispense()
    elif (int(message) >= 0 and int(message) <= 5):
        change_servings(message)
    elif (int(message) >= 10 and int(message) <= 60):
        delay_servings_min = int(message)
    else:
        print("Invalid message!")
  
def run():
    try:
        print("Loop start")
        # Start the MQTT loop
        client.loop()
    except Exception as e:
        print("Exception: ", e)
        sleep(6000)

try:
    # Connection to the wifi
    print("Configuring wifi. . .")
    wifi.configure(ssid, password)
    print("Connecting to wifi. . .")
    wifi.start()  
    print("Connected!")  
    print("Info: ", wifi.info())

    # The Agent class implements all the logic to talk with the ZDM
    agent = zdm.Agent(jobs={"close_servo":close_servo_manually})
    # Just start it
    agent.start()
    # The agent automatically handles connections and reconnections
    print("ZDM is online:    ",agent.online())
    # And provides info on the current firmware version
    print("Firmware version: ",agent.firmware())

    # Connection to the MQTT server
    client = mqtt.MQTT("test.mosquitto.org", "Gruppo05")
    # client.on registers the client to the topic and calls the callback function when an event occurs on that topic
    print("Subscribed to", sub, client.on(sub,callback,1))
    client.connect()  
    thread(run)

    cnt=0
    while True:
        sleep(5000)
        if client.is_connected():
            break
        cnt +=1
        print("Waiting connection...", cnt)
        if cnt > 10:
            print("Client not connected")
except Exception as e:
    raise e 

# the NTP protocol can be used to sync the clock 
# when internet access is available
ntp.sync_time(server="0.pool.ntp.org")

# Setting the timezone to UTC+2
ti_last_serving = time.localtime()
tinfo = time.TimeInfo()
tinfo.tm_year = ti_last_serving.tm_year
tinfo.tm_mon = ti_last_serving.tm_mon
tinfo.tm_mday = ti_last_serving.tm_mday
tinfo.tm_hour = ti_last_serving.tm_hour + 2
tinfo.tm_min = ti_last_serving.tm_min
tinfo.tm_sec = ti_last_serving.tm_sec
time.settime(tinfo)

# Turn on and set up the oled display
oled.begin()
oled.print("Welcome to FeedMyPet", True)
oled.print("Please set the", 0, 2, False)
oled.print("number of servings", 0, 3, False)
oled.print("from the App!", 0, 4, False)

# Reset GRAFANA datas
agent.publish({"total_servings":0, "manual_servings":0, "auto_servings":0}, "servings")

# Loop
while True:
    ti = time.localtime()
    value = gpio.get(pir_pin)
    # The servo only moves if the delay set in the App has passed
    if (value == HIGH and servings < servings_max and ((ti.to_tuple()[4] - ti_last_serving_min) >= delay_servings_min) and servings_max != 0):
        print("Movement detected")
        movement_detected()
    if (value == HIGH and (servings_max - servings) == 0):
        agent.publish({"no_servings": 1})