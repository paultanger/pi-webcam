#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import sys

button_pin = 27

GPIO.setmode(GPIO.BCM)

# https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/

'''
The pull_up_down parameter in the GPIO.setup call tells the Raspberry Pi which 
state the pin should be in when there is nothing connected to the pin. 
This is important since we want our program to read a low state when the 
button is not pushed and a high state when the button is pushed.
'''

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

'''
We want to rewrite our program to output a single message whenever the button 
is pressed rather than continuously outputting a message. 
To do this we need to use GPIO events.

A GPIO event in the Raspberry Pi Python GPIO library works by calling 
a Python function whenever an event is triggered. 
Such a function is called a callback function.

An event can be an input pin being low or high, but it could 
also be when the pin changes from low to high – called rising – 
or when the pin changes from high to low – called falling.

In our case we want to detect when the button is being pressed, 
that is going from low to high also called the rising edge.

'''


def button_callback(channel): # channel is what pin triggered callback
    print(f"Button was pushed triggered by pin : {channel}")


# GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_callback)


if __name__ == '__main__':

    button_pin = 27

    # try:
    #     while True:
    #         pass
    # except:
    #     GPIO.cleanup()

    GPIO.add_event_detect(button_pin, GPIO.RISING, callback=button_callback)
    message = input("Press enter to quit\n\n")
    GPIO.cleanup()

    # try:
    #     print('starting..')
    # except KeyboardInterrupt:
    #     GPIO.cleanup()

    # try:
    #     while True: # Run forever
    #         if GPIO.input(button_pin) == GPIO.HIGH:
    #             print("Button was pushed!")
    #             time.sleep(2)
    #         else:
    #             print('button not pushed')
    #             time.sleep(2)
    # except KeyboardInterrupt:
    #     GPIO.cleanup()