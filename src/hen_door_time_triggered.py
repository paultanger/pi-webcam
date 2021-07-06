#!/usr/bin/env python3

# this script checks time and opens or closes door as appropriate..

import RPi.GPIO as GPIO
import time
import sys
import logging
import time
import datetime
# import hen door funs
sys.path.insert(0, '../src/')
import hen_door as door_funcs

# setup pins
open_door_pin = 17
close_door_pin = 18

# setup hen door - these are pins
door_funcs.setup(open_door_pin, close_door_pin)

def main(open_time, close_time):
    '''
    function to control hen door
    params are open and close times in datetime format
    runs forever (while loop)
    '''

    logging.info('starting hen door func...')
    # setup current_time
    current_time = datetime.datetime.now().replace(microsecond=0).time()
    logging.info(f'setting hen door func current time as {current_time}')

    # setup current status of door..
    # TODO: how do we determine this??
    # this only gets complicated if we start pi and door is closed
    # when it should be open..
    # assume it is in correct position..
    # TODO: maybe we can track the time in each direction to correct if needed
    # and also to define time limits in both direction just in case..
    if current_time >= open_time and current_time <= close_time:
        door_open = True
        logging.info(f'setting door as open because: current time is {current_time}'
                     f' and open time is {open_time} and close time is {close_time}')
    else:
        door_open = False
        logging.info(f'setting door as closed because: current time is {current_time}' 
                     f' and open time is {open_time} and close time is {close_time}')

    # setup while forever to keep checking time..
    while True:
        # logging.info('starting or continuing hen door while loop to check time...')
        # check time
        current_time = datetime.datetime.now().replace(microsecond=0).time()
        # logging.info(f'current time is: {current_time}')

        # if time is in range..
        if current_time >= open_time and current_time <= close_time and door_open == False:
            # then open door..
            try:
                door_funcs.setup(open_door_pin, close_door_pin)
                door_funcs.activate_door('close', 26, open_door_pin, close_door_pin)
                logging.info(f'opening door.. because current time is {current_time}')
                door_open = True
            except:
                return None
        elif current_time >=close_time and door_open == True:
            # then close door..
            try:
                door_funcs.setup(open_door_pin, close_door_pin)
                door_funcs.activate_door('open', 25, open_door_pin, close_door_pin)
                logging.info(f'closing door..because current time is {current_time}')
                door_open = False
            except:
                return None
        else:
            # logging.info(f'waiting because open or close conditions not met and current time is {current_time}')
            pass

        # then wait 2.5 mins before checking again
        # logging.info(f'waiting for 2.5 mins because current time is {current_time}')
        time.sleep(150)
        current_time = datetime.datetime.now().replace(microsecond=0).time()
        # logging.info(f'ok done waiting because current time is {current_time}')
        # logging.info(f'now we go back to start of while loop because current time is {current_time}')
        

if __name__ == '__main__':
    # for log..
    logging.basicConfig(level=logging.DEBUG, 
                        filename="/etc/python_log_files/door_log.log", 
                        filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info('-------------------------------------------------------------')
    logging.info('----------------- new door log instance ---------------------')
    logging.info('-------------------------------------------------------------')
    # setup open and close times
    open_time = datetime.datetime.now().replace(hour=6, minute=30, second=0, microsecond=0).time()
    close_time = datetime.datetime.now().replace(hour=21, minute=0, second=0, microsecond=0).time()
    # just run this indefinately..
    main(open_time, close_time)