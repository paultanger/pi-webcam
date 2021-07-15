#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import sys

# setup pins
open_door_pin = 17
close_door_pin = 18
button_pin = 10

def setup(open_door_pin, close_door_pin, button_pin=10):
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    # Set pin mode to output, and initial level to High(3.3v)
    GPIO.setup(open_door_pin, GPIO.OUT, initial=0)

    # do the same for control of other direction
    GPIO.setup(close_door_pin, GPIO.OUT, initial=0)

    # and button pin
    # low state when not pushed, high state when pushed
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def activate_door(open_or_close, on_time, open_door_pin=17, close_door_pin=18,
                    button_pin=10):
    
    # Setup event on pin 10 rising edge
    GPIO.add_event_detect(button_pin,
                            GPIO.RISING,
                            # later add a func to do things when triggered..
                            callback=print('button triggered'))

    # while event not true?

    # while True:
    if open_or_close == 'close':
        print ('motor close door')
        GPIO.output(open_door_pin, GPIO.HIGH)
        GPIO.output(close_door_pin, GPIO.LOW)
        time.sleep(on_time)
        destroy(open_door_pin, close_door_pin, button_pin)

    if open_or_close == 'open':
        print ('motor open door')
        GPIO.output(open_door_pin, GPIO.LOW)
        GPIO.output(close_door_pin, GPIO.HIGH)
        time.sleep(on_time)
        destroy(open_door_pin, close_door_pin, button_pin)


# Define a destroy function for clean up everything after the script finished
def destroy(open_door_pin, close_door_pin, button_pin):
    # Turn off
    GPIO.output(open_door_pin, 0)
    GPIO.output(close_door_pin, 0)
    GPIO.output(button_pin, 0)
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

    setup()

    try:
        activate_door(the_command, on_time)
    # When 'Ctrl+C' is pressed, the program destroy() will be  executed.
    except KeyboardInterrupt:
        destroy()