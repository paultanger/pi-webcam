# this script checks if camera is accessible,
# if it is, that means it is not streaming and object detection isn't happening
# so then it checks a couple frames, and then sleeps for 5 minutes
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
    # setup current_time
    current_time = datetime.datetime.now().replace(second=0, microsecond=0)
    # possible predictions, this is a set
    egg_labels = {'sports ball', 'orange', 'apple', 'bowl', 'clock', 'mouse', 'bird'}
    # setup first text time when this script starts, minus 30 mins
    mins_30 = datetime.timedelta(minutes=30) 
    text_time = current_time - mins_30
    # setup morning time range
    start = datetime.datetime.now().replace(hour=6, minute=30, second=0, microsecond=0)
    end = datetime.datetime.now().replace(hour=21, minute=30, second=0, microsecond=0)

    while True:
        # while we are still checking frames
        #TODO: while 
        # setup current time
        current_time = datetime.datetime.now().replace(second=0, microsecond=0)
        # if haven't texted lately..
        time_diff = (datetime.datetime.now() - text_time).total_seconds()
        min_diff = divmod(time_diff, 60)[0]
        # if time in range, check if camera available
        if current_time <= end and current_time >= start and time_diff >= 30:
            # if it is, run obj detect
            rval, frame = vc.read() 
            bbox, label, conf = cv.detect_common_objects(frame, confidence=.3, model='yolov4-tiny')
            if label != []:
                labels = [lab for lab in label if lab in egg_labels]
                # only keep labels in this group
                label_count = Counter(labels)
                if len(label_count) > 1:
                # # determine if I have been texted in the last 30 mins?
                # time_diff = (datetime.now() - text_time).total_seconds()
                # min_diff = divmod(time_diff, 60)[0]
                # if min_diff >= 30:
                    # text me..
                    message = client.messages \
                    .create(
                        body = "a possible egg!",
                        from_= twilio_phone,
                        to = my_phone
                    )
                    # text Levitie
                    # message = client.messages \
                    # .create(
                    #     body = "a possible egg!",
                    #     from_= twilio_phone,
                    #     to = lev_phone
                    # )
                    # text Dorothy
                    # message = client.messages \
                    # .create(
                    #     body = "testing hen cam",
                    #     from_= twilio_phone,
                    #     to = dor_phone
                    # )
                    # restart time to wait 30 mins before doing again
                    text_time = datetime.datetime.now().replace(second=0, microsecond=0)
            # if we didn't trigger anything, check 10 more frames,
                # TODO...
            # then wait 5 mins before checking again
            print('checked 10 frame, waiting 5 mins..')
            # for testing:
            time.sleep(3)
            #time.sleep(300)



if __name__ == '__main__':
    main()