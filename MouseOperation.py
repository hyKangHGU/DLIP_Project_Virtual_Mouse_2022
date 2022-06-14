from Defines import *
import time
import cv2 as cv
import numpy as np
import autopy as ap
import pyautogui as pg

def cal_1Ddist(x1, x2):
    return abs(x2 - x1)

def cal_2Ddist(p1, p2):
    dist_x = cal_1Ddist(p1[0], p2[0])**2
    dist_y = cal_1Ddist(p1[1], p2[1])**2

    return (dist_x + dist_y)**0.5

def convert_coordinates(xVal, yVal):
    x = np.interp(xVal, (0, wCam),(0, W_SCR))
    y = np.interp(yVal, (0, hCam),(0, H_SCR))
    return x, y

def limit_cursor_location(clocX, clocY):
    if      clocX >= W_SCR  :   clocX = W_SCR - 1
    elif    clocX <= 0      :   clocX = 1
            
    if      clocY >= H_SCR  :   clocY = H_SCR - 1
    elif    clocY <= 0      :   clocY = 1

    return clocX, clocY

def get_current_location(x, y, plocX, plocY, pconX, pconY, fingers_prev):
    # Convert Coordinates
    cconX, cconY = convert_coordinates(x, y)
    
    # get current location
    if fingers_prev == False:
        clocX = plocX
        clocY = plocY
    else:
        clocX = plocX + (cconX - pconX) / smoothening_x
        clocY = plocY + (cconY - pconY) / smoothening_y

    # if the location change is very small, mouse cursor should not move
    if abs(clocX - plocX) < MIN_CHNAGE_DISTANCE:  clocX = plocX
    if abs(clocY - plocY) < MIN_CHNAGE_DISTANCE:  clocY = plocY

    # Limit mouse location not to exceed screen size
    clocX, clocY = limit_cursor_location(clocX, clocY)

    return clocX, clocY, cconX, cconY

def click_mouse_left(pMode, cMode, img, lineInfo, dist_ratio_56, dist_ratio_58):
    # Click mouse if distance condition is satisfied
    if dist_ratio_56 > MIN_NUM56_DISTANCE:
        if dist_ratio_58 < MIN_NUM58_DISTANCE:
            if pMode != MOUSE_L_CLICKING:
                cv.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv.FILLED)
                ap.mouse.click()
                pMode = MOUSE_L_CLICKING     
        else:
            pMode = cMode

    return pMode

def click_mouse_right(pMode, cMode, img, lineInfo, dist_ratio_56, dist_ratio_58):
    # Click mouse if distance condition is satisfied
    if dist_ratio_56 > MIN_NUM56_DISTANCE:
        if dist_ratio_58 < MIN_NUM58_DISTANCE:
            if pMode != MOUSE_R_CLICKING:
                cv.circle(img, (lineInfo[4], lineInfo[5]), 15, GREEN, cv.FILLED)
                pg.click(button = 'right')
                pMode = MOUSE_R_CLICKING
        else:
            pMode = cMode
    return pMode

def print_mode(cMode, img):
    if      cMode == NO_MODE            :   text = "NONE"
    elif    cMode == MOUSE_MOVE         :   text = "Moving"
    elif    cMode == MOUSE_L_CLICK_WAIT :   text = "Left Click (wait)"
    elif    cMode == MOUSE_L_CLICKING   :   text = "Left Click"
    elif    cMode == MOUSE_R_CLICK_WAIT :   text = "Right Click (wait)"
    elif    cMode == MOUSE_R_CLICKING   :   text = "Right Click"
    elif    cMode == MOUSE_DRAG_DOWN    :   text = "Drag On"
    elif    cMode == MOUSE_DRAG_UP      :   text = "Drag Off"
    elif    cMode == SCROLL_WAIT        :   text = "Scroll (wait)"
    elif    cMode == SCROLL_MOVE        :   text = "Scroll"
    elif    cMode == MIDDLE_FINGER_UP   :   text = "Don't say swear words ..."

    cv.putText(img, text, (100,50), cv.FONT_HERSHEY_PLAIN, 2, RED, 3)

def check_show_time(img, pTime):
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv.putText(img, str(int(fps)), (20, 50), cv.FONT_HERSHEY_PLAIN, 3, BLUE, 3)
    return pTime

def print_save_files():
    time_str_HMS = time.strftime("%H:%M:%S")
    print("\nSaved video file at " + time_str_HMS)
    print("Saved text log file at " + time_str_HMS + "\n")
