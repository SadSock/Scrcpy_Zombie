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
import time


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

pos_结束挑战_x = 273
pos_结束挑战_y = 990


pos_进入招募_x = 503
pos_进入招募_y = 618


pos_基地_x = 370
pos_基地_y = 1151


pos_历练大厅_x = 100
pos_历练大厅_y = 450


pos_环球救援_x = 300
pos_环球救援_y = 625


pos_环球救援_开始游戏_x = 280
pos_环球救援_开始游戏_y = 1120


# 检测图像是否发生变化的矩形区域
top_left_x = 40
top_left_y = 400
bottom_right_x = 120
bottom_right_y = 580




#enter_base_command = "adb shell input tap " + str(pos_base_x * scale_ratio) + " " + str(pos_base_y * scale_ratio)

#enter_hall_command = "adb shell input tap " + str(pos_hall_x * scale_ratio) + " " + str(pos_hall_y * scale_ratio)

#enter_rescue_command = "adb shell input tap " + str(pos_rescue_x * scale_ratio) + " " + str(pos_rescue_y * scale_ratio)

#enter_recruit_command = "adb shell input tap " + str(pos_recruit_x * scale_ratio) + " " + str(pos_recruit_y * scale_ratio)




cap = cv2.VideoCapture(0)


if not cap.isOpened():
    print("do not open camera\n")
    exit(-1)


template_rescue = cv2.imread("../resource/template_rescue.png")
template_环球救援 = cv2.imread("../resource/template_global_rescue.bmp")
template_挑战失败 = cv2.imread("../resource/template_challenging_failure.bmp")
template_挑战成功 = cv2.imread("../resource/template_challenging_success.bmp")
template_组队招募 = cv2.imread("../resource/template_recruit.bmp")
template_战斗    = cv2.imread("../resource/template_battle.bmp")


h,w = template_rescue.shape[:-1]
pos_old_rescue_y = 20

#subprocess.run(enter_base_command, shell=True)
#subprocess.run(enter_hall_command, shell=True)
#subprocess.run(enter_rescue_command, shell=True)
#subprocess.run(enter_recruit_command, shell=True)
status = "组队招募"
frame_cnt = 0
threshold = 0.8

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
    
    
    if(frame_cnt == 1):
        # 保存上一帧的片段，用来检测图像是否发生变化
        pre_roi =  frame_scale[top_left_y : bottom_right_y, top_left_x:bottom_right_x]
        #cv2.imshow('zombie', pre_roi)
        #if cv2.waitKey(1) == ord('q'):
        #    break

        
    ## 确定当前所处的状态
    
    if(frame_cnt % 20 == 0):
        
        # 环球救援
        result = cv2.matchTemplate(frame_scale, template_环球救援, cv2.TM_CCOEFF_NORMED)
        locations = np.where(abs(result) >= 0.89)
        locations = list(zip(*locations[::-1]))
        # find rescue
        if(len(locations)!=0):
            status="环球救援"
            logging.info("status:" + status + " " + str(np.max(abs(result))))
            status="环球救援"
            
        result = cv2.matchTemplate(frame_scale, template_挑战失败, cv2.TM_CCOEFF_NORMED)
        locations = np.where(abs(result) >= threshold)
        locations = list(zip(*locations[::-1]))
        # find rescue
        if(len(locations)!=0):
            status="挑战结束"
            logging.info(status)
        
        result = cv2.matchTemplate(frame_scale, template_挑战成功, cv2.TM_CCOEFF_NORMED)
        locations = np.where(abs(result) >= threshold)
        locations = list(zip(*locations[::-1]))
        # find rescue
        if(len(locations)!=0):
            status="挑战结束"
            logging.info(status)
    
    
        result = cv2.matchTemplate(frame_scale, template_组队招募 , cv2.TM_CCOEFF_NORMED)
        locations = np.where(abs(result) >= threshold)
        locations = list(zip(*locations[::-1]))
        # find rescue
        if(len(locations)!=0):
            status="组队招募"
            logging.info(status)

        result = cv2.matchTemplate(frame_scale, template_战斗, cv2.TM_CCOEFF_NORMED)
        locations = np.where(abs(result) >= threshold)
        locations = list(zip(*locations[::-1]))
        # find rescue
        if(len(locations)!=0):
            status="战斗"
            logging.info(status)        
    
    
    if(status=="战斗"):
        enter_基地_command = "adb shell input tap " + str(pos_基地_x * scale_ratio) + " " + str(pos_基地_y * scale_ratio)
        subprocess.run(enter_基地_command, shell=True)
        time.sleep(0.2)
        enter_历练大厅_command = "adb shell input tap " + str(pos_历练大厅_x * scale_ratio) + " " + str(pos_历练大厅_y * scale_ratio)
        subprocess.run(enter_历练大厅_command, shell=True)
        time.sleep(0.2)
        enter_环球救援_command = "adb shell input tap " + str(pos_环球救援_x * scale_ratio) + " " + str(pos_环球救援_y * scale_ratio)
        subprocess.run(enter_环球救援_command, shell=True)
        #time.sleep(0.2)
        status="环球救援"
        
    
    if(status=="环球救援"):
        enter_环球救援_开始游戏_command = "adb shell input tap " + str(pos_环球救援_开始游戏_x * scale_ratio) + " " + str(pos_环球救援_开始游戏_y * scale_ratio)
        subprocess.run(enter_环球救援_开始游戏_command, shell=True)
        status="环球救援战斗中"
        
    if(status=="挑战结束"):
        exit_挑战结束_command = "adb shell input tap " + str(pos_结束挑战_x * scale_ratio) + " " + str(pos_结束挑战_y * scale_ratio)
        subprocess.run(exit_挑战结束_command, shell=True)
        status=""
    
    if(status=="组队招募"):
        result = cv2.matchTemplate(frame_scale, template_rescue, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        locations = np.where(abs(result) >= threshold)
        locations = list(zip(*locations[::-1]))
        
        cur_roi =  frame_scale[top_left_y : bottom_right_y, top_left_x : bottom_right_x]
        result = cv2.matchTemplate(cur_roi, pre_roi, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        pre_roi = cur_roi
        
        
        loginfo = "组队招募屏幕相似度: " + str(max_val)
        logging.info(loginfo)
        
        if(max_val > 0.99):
            continue
        
            
        for i in range(len(locations)):
            pt = locations[i]            
            loginfo = "环球救援屏幕坐标: " + str(pt[1]) + "（新） " +  str(pos_old_rescue_y) + "（旧）" 
            logging.info(loginfo)
            

            rob_rescue_command = "adb shell input tap " + str((pt[0] + w) * scale_ratio) + " " + str((pt[1] + h) * scale_ratio)
            # 找到环球救援之后，单击click_num次
            click_num = 1 
            for i in range(click_num):   
                subprocess.run(rob_rescue_command, shell=True)
            
    #保存图片
    if(frame_cnt % 100 == 0):        
        cv2.imwrite("../images/"+str(frame_cnt / 1000  % 1000 )+".bmp", frame_scale)
        loginfo = "保存 " + "../images/"  + str(frame_cnt / 1000  % 1000 )+".bmp"
        logging.info(loginfo)
    #cv2.imshow('zombie', frame_sc
    #cv2.imshow('zombie', frame_scale)
    #if cv2.waitKey(1) == ord('q'):
    #    break

cap.release()
cv2.destroyAllWindows()
