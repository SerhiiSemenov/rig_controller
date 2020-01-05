import OPi.GPIO as GPIO

class Relay:
    def __init__(self):
        print("Relay")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(3, GPIO.OUT)
        GPIO.setup(5, GPIO.OUT)

    def relay_off():
        print("relay_off")
        GPIO.output(3, GPIO.LOW)
        GPIO.output(5, GPIO.LOW)

    def relay_on():
        print("relay_on")
        GPIO.output(3, GPIO.HIGH)
        GPIO.output(5, GPIO.HIGH)
