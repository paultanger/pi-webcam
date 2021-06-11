#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import sys

# setup pins
open_door_pin = 17
close_door_pin = 18

def setup():
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    # Set pin mode to output, and initial level to High(3.3v)
    GPIO.setup(open_door_pin, GPIO.OUT, initial=GPIO.HIGH)

    # do the same for control of other direction
    GPIO.setup(close_door_pin, GPIO.OUT, initial=GPIO.HIGH)


def activate_door(open_or_close):
    # while True:
    #     print ('motor open door')
    #     GPIO.output(open_door_pin, GPIO.LOW)
    #     #GPIO.output(close_door_pin, GPIO.LOW)
    #     time.sleep(3)
    #     print ('motor close door')
    #     GPIO.output(open_door_pin, GPIO.HIGH)
    #     #GPIO.output(close_door_pin, GPIO.HIGH)
    #     time.sleep(2)
    

    if open_or_close == 'open':
        print ('motor open door')
        GPIO.output(open_door_pin, GPIO.LOW)
        #GPIO.output(close_door_pin, GPIO.LOW)
        time.sleep(3)

    if open_or_close == 'close':
        print ('motor close door')
        GPIO.output(open_door_pin, GPIO.HIGH)
        GPIO.output(close_door_pin, GPIO.HIGH)
        time.sleep(2)


# Define a destroy function for clean up everything after the script finished
def destroy():
    # Turn off
    GPIO.output(open_door_pin, GPIO.HIGH)
    GPIO.output(close_door_pin, GPIO.HIGH)
    # Release resource
    GPIO.cleanup()


if __name__ == '__main__':
    the_command = sys.argv[1]
    print(the_command)

    setup()

    try:
        activate_door(the_command)
    # When 'Ctrl+C' is pressed, the program destroy() will be  executed.
    except KeyboardInterrupt:
        destroy()