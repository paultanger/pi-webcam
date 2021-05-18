# this script checks if camera is accessible,
# if it is, that means it is not streaming and object detection isn't happening
# so then it checks 10 frames, and then sleeps for 5 minutes
# it does this only during certain egg laying hours

# this script also needs to be started separately from the app..

import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import picamera
import time
import datetime
from collections import Counter
from twilio.rest import Client
import logging
import sys, os
sys.path.insert(0, '../src/')
import funcs as myfuncs

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_phone = os.environ['TWILIO_PHONE_NUM']
my_phone = os.environ['MY_PHONE_NUM']
mer_phone = os.environ['MER_PHONE_NUM']
lev_phone = os.environ['LEV_PHONE_NUM']
dor_phone = os.environ['DOR_PHONE_NUM']

client = Client(account_sid, auth_token)

def main():
    logging.info('starting main func..')
    # setup current_time
    current_time = datetime.datetime.now().replace(second=0, microsecond=0)
    logging.info(f'setting func start time as {current_time}')
    # possible predictions, this is a set
    egg_labels = {'sports ball', 'orange', 'apple', 'bowl', 'clock', 'mouse'}
    # setup first text time when this script starts, minus 30 mins
    mins_30 = datetime.timedelta(minutes=30) 
    text_time = current_time - mins_30
    logging.info(f'setting text_time as {text_time}')
    # setup morning time range
    start = datetime.datetime.now().replace(hour=7, minute=15, second=0, microsecond=0)
    end = datetime.datetime.now().replace(hour=16, minute=30, second=0, microsecond=0)

    while True:
        # logging.info('starting while loop')
        # while we are still checking frames.. check 10
        for i in range(10):
            # logging.info(f'starting for loop for 10 frames iter: {i}')
            # setup current time
            # current_time = datetime.datetime.now().replace(second=0, microsecond=0)
            # if haven't texted lately..
            time_diff = (datetime.datetime.now() - text_time).total_seconds()
            min_diff = divmod(time_diff, 60)[0]
            # logging.info(f'time between current time and text time is: {min_diff} mins')
            # if time in range, check if camera available
            #breakpoint()
            vc = cv2.VideoCapture(0)
            time.sleep(1)
            if current_time <= end and current_time >= start and min_diff >= 30 and vc.isOpened() == True:
                # logging.info('in if stmt to run obj detect')
                # if it is, run obj detect
                rval, frame = vc.read() 
                
                # flip frame (depending on how we setup the camera)
                frame = cv2.flip(frame, 0)

                bbox, label, conf = cv.detect_common_objects(frame, confidence=.3, model='yolov4-tiny')
                if label != []:
                    # logging.info('something predicted..')
                    labels = [lab for lab in label if lab in egg_labels]
                    # only keep labels in this group
                    label_count = Counter(labels)
                    # setup two test cases to check
                    # label_count = {'bird': 2}
                    # label_count = {'bird':1, 'clock':1}
                    # label_count = Counter() # this is an empty.. it shouldn't get here, but for some reason sometimes it does
                    if len(label_count) > 1 or max(label_count.values(), default=-999) > 1:
                        logging.info('sending text..')
                        # text me..
                        message = client.messages \
                        .create(
                            body = "a possible egg! via detect script",
                            from_= twilio_phone,
                            to = my_phone
                        )
                        # text Levitie
                        message = client.messages \
                        .create(
                            body = "a possible egg! via detect script",
                            from_= twilio_phone,
                            to = lev_phone
                        )
                        # # text Dorothy
                        message = client.messages \
                        .create(
                            body = "a possible egg! via detect script",
                            from_= twilio_phone,
                            to = dor_phone
                        )
                        # restart time to wait 30 mins before doing again
                        text_time = datetime.datetime.now().replace(second=0, microsecond=0)
                        logging.info(f'resetting text time to: {text_time}')
                        # wait so we don't check any more frames..
                        time.sleep(3)
                # if we didn't trigger anything, check 10 more frames...
                # close our attempt at vc
                vc.release()
            else:
                pass
                # logging.info('time not in range, or texted recently or vc not available')
        # then wait 5 mins before checking again
        # logging.info('checked 10 times, waiting 5 mins..')
        # for testing:
        #time.sleep(3)
        time.sleep(300)


if __name__ == '__main__':
    # for log..
    logging.basicConfig(level=logging.DEBUG, 
                        filename="/etc/python_log_files/obj_det.log", 
                        filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
    logging.info('-------------------------------------------------------------')
    logging.info('----------------- new obj detect instance -------------------')
    logging.info('-------------------------------------------------------------')
    # just run this indefinately..
    # python run_obj_detect.py
    main()