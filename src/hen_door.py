#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import sys

# setup pins
open_door_pin = 17
close_door_pin = 18

# with new relay, it has default pins.. not sure how to change..
# http://www.ingcool.com/wiki/RPi_Relay_Board?Amazon
# ch 3 is pin 21 in case I need it later..
open_door_pin = 26
close_door_pin = 20 

def setup(open_door_pin, close_door_pin):
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    # Set pin mode to output, and initial level to High(3.3v)
    GPIO.setup(open_door_pin, GPIO.OUT, initial=0)

    # do the same for control of other direction
    GPIO.setup(close_door_pin, GPIO.OUT, initial=0)


def activate_door(open_or_close, on_time, open_door_pin=26, close_door_pin=20):
    
    # while True:
    if open_or_close == 'close':
        print ('motor close door')
        GPIO.output(open_door_pin, GPIO.HIGH)
        GPIO.output(close_door_pin, GPIO.LOW)
        time.sleep(on_time)
        destroy(open_door_pin, close_door_pin)

    if open_or_close == 'open':
        print ('motor open door')
        GPIO.output(open_door_pin, GPIO.LOW)
        GPIO.output(close_door_pin, GPIO.HIGH)
        time.sleep(on_time)
        destroy(open_door_pin, close_door_pin)


# Define a destroy function for clean up everything after the script finished
def destroy(open_door_pin, close_door_pin):
    # Turn off
    GPIO.output(open_door_pin, 0)
    GPIO.output(close_door_pin, 0)
    # Release resource
    GPIO.cleanup()


if __name__ == '__main__':
    # run with:
    # python hen_door.py open 25
    # python hen_door.py close 25
    
    the_command = sys.argv[1]
    on_time = float(sys.argv[2])
    print(the_command)
    print(on_time)

    open_door_pin = 17
    close_door_pin = 18

    open_door_pin = 26
    close_door_pin = 20 

    setup(open_door_pin, close_door_pin)

    try:
        activate_door(the_command, on_time, open_door_pin, close_door_pin)
    # When 'Ctrl+C' is pressed, the program destroy() will be  executed.
    except KeyboardInterrupt:
        destroy(open_door_pin, close_door_pin)