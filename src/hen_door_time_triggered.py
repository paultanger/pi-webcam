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

def main():
    logging.info('starting hen door func...')
    # setup current_time
    current_time = datetime.datetime.now().replace(second=0, microsecond=0)
    logging.info(f'setting hen door func start time as {current_time}')
    # setup open and close times
    open_time = datetime.datetime.now().replace(hour=7, minute=00, second=0, microsecond=0)
    close_time = datetime.datetime.now().replace(hour=21, minute=15, second=0, microsecond=0)
    while True:
        # setup while forever..
        logging.info('starting or continuing hen door while loop to check time...')
        # setup door status
        # TODO: how do we determine this??
        # this only gets complicated if we start pi and door is closed
        # when it should be open..
        # assume it is in correct position..
        # resetting current time
        current_time = datetime.datetime.now().replace(second=0, microsecond=0)
        logging.info(f'resetting current time as {current_time} and open time is {open_time} and close time is {close_time}')
        if current_time >= open_time and current_time <= close_time:
            door_open = True
            logging.info(f'setting door as open because: current time is {current_time} and open time is {open_time} and close time is {close_time}')
        else:
            door_open = False
            logging.info(f'setting door as closed because: current time is {current_time} and open time is {open_time} and close time is {close_time}')

        logging.info(f'door open time is: {open_time} and close time is {close_time}')
        for i in range(5): # 86400 seconds per day.. or just check for 5 secs?
            # check time
            current_time = datetime.datetime.now().replace(second=0, microsecond=0)
            logging.info(f'current time is: {current_time}')
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
                logging.info(f'waiting because open or close conditions not met and current time is {current_time}')
                pass

            # then wait 2.5 mins before checking again
            logging.info(f'waiting for 2.5 mins because current time is {current_time}')
            time.sleep(150)
            current_time = datetime.datetime.now().replace(second=0, microsecond=0)
            logging.info(f'ok done waiting because current time is {current_time}')
        logging.info(f'now we are done with the for loop for 5 tries because current time is {current_time}')
        

if __name__ == '__main__':
    # for log..
    logging.basicConfig(level=logging.DEBUG, 
                        filename="/etc/python_log_files/door_log.log", 
                        filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info('-------------------------------------------------------------')
    logging.info('----------------- new door log instance ---------------------')
    logging.info('-------------------------------------------------------------')
    # just run this indefinately..
    main()