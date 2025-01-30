# -*- coding: utf-8 -*-
"""
Spyder 编辑器

这是一个临时脚本文件。
"""

import cv2
import numpy as np
from scipy.spatial import distance
import mss
import pygetwindow as gw  # 用于获取窗口位置
import time
import logging
import pyautogui
from tinydb import TinyDB, Query
from datetime import datetime






pyautogui.FAILSAFE = True


obj_width = 1164 / 2
obj_height = 2064 /2


pos_基地_x = 369
pos_基地_y = 978

pos_历练大厅_x = 120
pos_历练大厅_y = 480

pos_环球挑战_x = 384
pos_环球挑战_y = 635

pos_聊天_x = 530
pos_聊天_y = 513

pos_招募_x = 111
pos_招募_y = 274

pos_返回 = (290,890)

pos_skills = [(114,487), (284,485), (481, 492) ]

pos_组队招募_sample = [(193, 281), ]

pts = None
ratio_width = 0.0
ratio_height = 0.0
threshold = 0.9  # 设置匹配阈值
cnt = 0

status = ""

template_战斗 = cv2.imread('./resource/battle.bmp')
template_组队招募     = cv2.imread('./resource/recruitment.bmp')
template_寰球救援卡     = cv2.imread('./resource/rescue_card.bmp')
template_寰球救援     = cv2.imread('./resource/rescue.bmp')
template_奖励领取     = cv2.imread('./resource/rewards.bmp')
template_自动技能     = cv2.imread('./resource/auto_skill.bmp')




# 连接到 TinyDB 数据库，创建或打开一个 JSON 文件作为数据库
db = TinyDB('counter.json')
# 获取当天的日期并格式化为字符串，作为键
today = datetime.today().strftime('%Y-%m-%d')
# 创建一个查询对象
Entry = Query()
# 检查当天日期的数据点是否已经存在
entry = db.get(Entry.date == today)
if not entry:
    db.insert({'date': today, 'value': 0})


# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



# ===== 步骤1：获取微信小程序窗口的位置和尺寸 =====
def find_wechat_window():
    """
    查找微信窗口并返回其位置和尺寸
    """
    # 通过窗口标题模糊匹配微信窗口（标题可能因微信版本不同略有差异）
    windows = gw.getWindowsWithTitle("向僵尸开炮")
    if not windows:
        raise Exception("未找到微信窗口！请确保微信已打开并处于前台状态")
    
    # 选择第一个匹配的窗口
    wechat_window = windows[0]
    
    # 如果窗口最小化，先恢复
    if wechat_window.isMinimized:
        wechat_window.restore()
    
    # 将窗口置顶（可能需要管理员权限）
    #try:
    #    wechat_window.activate()
    #except Exception as e:
    #    print("警告：无法置顶窗口，确保窗口未被最小化")
    
    # 返回窗口坐标和尺寸
    return {
        "left": wechat_window.left,
        "top": wechat_window.top,
        "width": wechat_window.width,
        "height": wechat_window.height
    }



def template_match(template: np.ndarray)->bool:
    # 战斗
    #template_image = template_组队招募
    # 获取模板图像的尺寸
    template_height, template_width = template.shape[:2]
    # 使用模板匹配方法
    result = cv2.matchTemplate(scale_img , template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    
    # 匹配到的区域用红框标出
    #for pt in zip(*locations[::-1]):  # 遍历所有匹配位置
    #    cv2.rectangle(image, pt, (pt[0] + template_width, pt[1] + template_height), (0, 0, 255), 2)
    if(len(locations[0])>0):
        return True
    else:
        return False
    

def get_status(image: np.ndarray)->str:
    """
    处理输入的 OpenCV 图像，并返回一个描述图像信息的字符串。

    参数:
        image (np.ndarray): 输入的 OpenCV 图像。

    返回:
        str: 描述图像信息的字符串。如果输入无效，返回 None。
    """
    
    # 战斗
    template_image = template_战斗
    # 获取模板图像的尺寸
    template_height, template_width = template_image.shape[:2]
    # 使用模板匹配方法
    result = cv2.matchTemplate(image, template_image, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    
    # 匹配到的区域用红框标出
    #for pt in zip(*locations[::-1]):  # 遍历所有匹配位置
    #    cv2.rectangle(image, pt, (pt[0] + template_width, pt[1] + template_height), (0, 0, 255), 2)
    if(len(locations[0])>0):
        logging.info("get_status: 战斗" + "("+ str(len(locations[0]))   +")")
        return "战斗"
    
    

    
    return "未知"

def click_once(pos_x:int, pos_y:int):
    pos_x = pos_src["left"] + pos_x / ratio_width
    pos_y = pos_src["top"] + pos_y  / ratio_height
    pyautogui.click(pos_x, pos_y)
    logging.info("click:" + str(int(pos_x))+ str(int(pos_y)))

# ===== 步骤2：配置mss截图区域 =====
try:
    pos_src = find_wechat_window()
    print(f"捕获区域配置：{pos_src}")
except Exception as e:
    print(f"错误：{e}")
    print(">>> 请手动输入捕获区域 <<<")
    pos_src = {
        "left": int(input("左上角X坐标：")),
        "top": int(input("左上角Y坐标：")),
        "width": int(input("宽度：")),
        "height": int(input("高度："))
    }

# ===== 步骤3：实时捕获并显示 =====
with mss.mss() as sct:
    # 创建OpenCV窗口
    cv2.namedWindow("WeChat", cv2.WINDOW_NORMAL)
    
    # 设置帧率统计
    fps = 0
    last_time = time.time()
    
    while True:
        # 捕获屏幕
        screenshot = sct.grab(pos_src)
        
        # 转换为OpenCV格式（BGRA -> BGR）
        src_img = np.array(screenshot)
        src_img = cv2.cvtColor(src_img, cv2.COLOR_BGRA2BGR)
        
        
        
        
        # 计算实时帧率
        current_time = time.time()
        fps = 1 / (current_time - last_time)
        last_time = current_time
        
        # 缩小为原来的1/2
        ratio_height = obj_height * 1.0 / pos_src["height"]
        ratio_width = obj_width * 1.0  / pos_src["width"]
        
        
        scale_img = cv2.resize(src_img, None, fx=ratio_width, fy=ratio_height, interpolation=cv2.INTER_AREA)


        #
        if(pts == None):
            for i in range(len(pos_组队招募_sample)):
                pts = []
                pts.append(scale_img[pos_组队招募_sample[i][0], pos_组队招募_sample[i][1]])


        # 确定当前的状态
        if cnt % 100 == 0:
            if(template_match(template_寰球救援)):
                status="寰球救援"
            elif(template_match(template_战斗)):
                status="战斗"
            elif(template_match(template_奖励领取)):
                status="奖励领取"
            elif(template_match(template_组队招募)):
                status="组队招募"
            elif(template_match(template_自动技能)):
                status="自动技能"
            else:
                status="未知"
            logging.info("status:" + str(status))
            
        #logging.info("status:" + str(status)) 
        if(status=="战斗"):
            # 进入基地
            click_once(pos_基地_x, pos_基地_y)
            time.sleep(0.3)
            click_once(pos_历练大厅_x , pos_历练大厅_y)
            time.sleep(0.3)
            click_once(pos_历练大厅_x , pos_历练大厅_y)
            time.sleep(0.3)
            click_once(pos_环球挑战_x , pos_环球挑战_y)
            time.sleep(0.3)
            click_once(pos_聊天_x, pos_聊天_y)
            time.sleep(0.3)
            click_once(pos_招募_x , pos_招募_y)
            status="组队招募"
        elif(status=="组队招募"):
            #组队招募
            for i in range(len(pts)):
                pt = scale_img[pos_组队招募_sample[i][0], pos_组队招募_sample[i][1]]
                dis = cv2.norm(pt - pts[i], cv2.NORM_L2)
                #dis = distance(pt, pts[i])
                #logging.info("pt:"+ str(pt))
                if(dis >= 0):
                    logging.info("distance:"+ str(dis))
                    pts[i] = pt
                    cv2.circle(scale_img, (pos_组队招募_sample[i][0], pos_组队招募_sample[i][1]), radius=3, color=(0, 255, 0), thickness=2)

                    
                    # 战斗
                    template_image = template_寰球救援卡
                    # 获取模板图像的尺寸
                    template_height, template_width = template_image.shape[:2]
                    # 使用模板匹配方法
                    result = cv2.matchTemplate(scale_img, template_image, cv2.TM_CCOEFF_NORMED)
                    locations = np.where(result >= threshold)
                    
                    # 匹配到的区域用红框标出
                    for pt in zip(*locations[::-1]):  # 遍历所有匹配位置
                        click_once(pt[0], pt[1])
                        logging.info("抢: "+ "(%d,%d)"%(pt[0], pt[1]))
                        #cv2.rectangle(scale_img, pt, (pt[0] + template_width, pt[1] + template_height), (0, 0, 255), 2)
                    
                    break
        elif(status=="奖励领取"):
                #恭喜获得
                click_once(pos_返回[0], pos_返回[1])
                entry = db.get(Entry.date == today)
                value = entry['value'] + 1
                db.update({'value': value}, Entry.date == today)
                status="未知"
        elif(status=="寰球救援"):
                #恭喜获得
                click_once(pos_返回[0], pos_返回[1])
                click_once(pos_聊天_x, pos_聊天_y)
                time.sleep(0.3)
                click_once(pos_招募_x , pos_招募_y)
                status="组队招募"
        elif(status=="自动技能"):
            # 自动技能
            click_once(pos_skills[0][0], pos_skills[0][1])
            status="战斗中"
            
        else:
            a = 0




            
        # 在画面上叠加帧率信息
        cv2.putText(scale_img, 
                   f"FPS: {fps:.1f} | Press Q to exit",
                   (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX,
                   0.8,
                   (0, 255, 0),
                   2)
        
        # 显示画面
        cv2.imshow("WeChat", scale_img)
        cnt = cnt + 1
        if(cnt % 100==0):
            cv2.imwrite('./image/'+str(cnt)+'.bmp', scale_img)
        # 退出检测（按Q键退出）
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

# 释放资源
cv2.destroyAllWindows()