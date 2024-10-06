#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 16:08:52 2024

@author: xwu
"""


import cv2
import numpy as np
import subprocess
import logging
import sys



real_width  = 1080
real_height = 2400


vitual_width = 270
vitual_height = 600

scale_ratio = 2

pos_base_x = 403
pos_base_y = 1151

pos_hall_x = 102
pos_hall_y = 529

pos_rescue_x = 365
pos_rescue_y = 654


pos_recruit_x = 510
pos_recruit_y = 616


#enter_base_command = "adb shell input tap " + str(pos_base_x * scale_ratio) + " " + str(pos_base_y * scale_ratio)

#enter_hall_command = "adb shell input tap " + str(pos_hall_x * scale_ratio) + " " + str(pos_hall_y * scale_ratio)

#enter_rescue_command = "adb shell input tap " + str(pos_rescue_x * scale_ratio) + " " + str(pos_rescue_y * scale_ratio)

#enter_recruit_command = "adb shell input tap " + str(pos_recruit_x * scale_ratio) + " " + str(pos_recruit_y * scale_ratio)




cap = cv2.VideoCapture(0)


if not cap.isOpened():
    print("do not open camera\n")
    exit(-1)


template_rescue = cv2.imread("../resource/template_rescue.png")
h,w = template_rescue.shape[:-1]
pos_old_rescue_y = 20

#subprocess.run(enter_base_command, shell=True)
#subprocess.run(enter_hall_command, shell=True)
#subprocess.run(enter_rescue_command, shell=True)
#subprocess.run(enter_recruit_command, shell=True)
status = "组队招募"
frame_cnt = 0


# 配置日志，输出到控制台
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format='%(asctime)s - %(levelname)s - %(message)s'  # 日志格式
)



#logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)

while True:
    ret, frame = cap.read()
    frame_cnt = frame_cnt + 1

    #print(frame_cnt)
    if not ret:
        print("can not receive frame, quit\n")
        break
    
    
    real_height, real_width = frame.shape[:2]
    vitual_width = real_width // scale_ratio
    vitual_height = real_height // scale_ratio
    
    
    frame_scale = cv2.resize(frame, (vitual_width, vitual_height), interpolation=cv2.INTER_LINEAR)
    #cv2.namedWindow("zombie", cv2.WINDOW_NORMAL)
    #cv2.resizeWindow("zombie", real_width//4, real_height//4)
    
    
    logging.info(status)
    
    #logging.info("%s", status)
    
    if(status=="组队招募"):
        result = cv2.matchTemplate(frame_scale, template_rescue, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        
        
        # find rescue
        if(len(locations)!=0):
            
            pt = locations[0]
    
            print(pt[1], pos_old_rescue_y)
            
            loginfo = "环球救援屏幕坐标: " + str(pt[1]) + "（新） " +  str(pos_old_rescue_y) + "（旧）" 
            logging.info(loginfo)
            
    
            # not old rescue
            # pos_old_rescue_y is the rescue found in previous frame_scale
            # pt is the rescue found in current frame_scale        
            if not (pt[1] < pos_old_rescue_y + 10 and pt[1] > pos_old_rescue_y - 10):
                cv2.rectangle(frame_scale, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)
                rob_rescue_command = "adb shell input tap " + str((pt[0] + w) * scale_ratio) + " " + str((pt[1] + h) * scale_ratio)
                # 找到环球救援之后，单击click_num次
                click_num = 1 
                for i in range(click_num):   
                    subprocess.run(rob_rescue_command, shell=True)
            
            # 
            pos_old_rescue_y = pt[1]
        else:
            # not find rescue
            pos_old_rescue_y = 20
    #保存图片
    if(frame_cnt % 1000 == 0):        
        cv2.imwrite(str(frame_cnt / 1000  % 1000 )+".png", frame_scale)
        loginfo = "保存 " + str(frame_cnt / 1000  % 1000 )+".png"
        logging.info(loginfo)
    #cv2.imshow('zombie', frame_scale)
    #if cv2.waitKey(1) == ord('q'):
    #    break

cap.release()
cv2.destroyAllWindows()
