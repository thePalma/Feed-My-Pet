import gpio
import pwm

def angle2pulse(angle):
    return 1000+int(angle*1000/180)

servo_pin = D23

gpio.mode(servo_pin, OUTPUT)

period = 20000
angle = 0

def handle_servo(mode):
    if mode == "open":
        angle += 180
        pulse = angle2pulse(angle)
        #print("Angle = %d; pulse = %d" %(angle, pulse))
        pwm.write(servo_pin, period, pulse, MICROS)
        sleep(4000)
    if mode == "close":
        #initial position
        angle = 0
        pulse = angle2pulse(angle)
        #print("Angle = %d; pulse = %d" %(angle, pulse))
        pwm.write(servo_pin, period, pulse, MICROS)