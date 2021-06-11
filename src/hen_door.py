#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# setup pins
CW_pin = 17
CCW_pin = 18

def setup():
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    # Set LedPin's mode to output,and initial level to High(3.3v)
    GPIO.setup(CW_pin, GPIO.OUT, initial=GPIO.HIGH)

    # also do something with this other one
    GPIO.setup(CCW_pin, GPIO.OUT, initial=GPIO.HIGH)


def main():
    while True:
        print ('...LED ON')
        # Turn on LED
        GPIO.output(CW_pin, GPIO.LOW)
        #GPIO.output(CCW_pin, GPIO.LOW)
        time.sleep(3)
        print ('LED OFF...')
        # Turn off LED
        GPIO.output(CW_pin, GPIO.HIGH)
        #GPIO.output(CCW_pin, GPIO.HIGH)
        time.sleep(2)


# Define a destroy function for clean up everything after the script finished
def destroy():
    # Turn off LED
    GPIO.output(CW_pin, GPIO.HIGH)
    # Release resource
    GPIO.cleanup()


if __name__ == '__main__':
    setup()
    try:
        main()
    # When 'Ctrl+C' is pressed, the program destroy() will be  executed.
    except KeyboardInterrupt:
        destroy()