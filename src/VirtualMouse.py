import cv2 as cv
from Defines import *
from MouseOperation import *
from HandTrackingModule import *
import autopy as ap

# =================== 1. Initialization ================== #
cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = handDetector(maxHands=1)

print(W_SCR, H_SCR)

while True:
    # =================== 2. Hand Tracking ================== #
    # 2-1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2-2. Check the hand detected
    if len(lmList) != 0:

        # =================== 3. Mode update ================== #
        # 3-1. Check which fingers are up
        fingers = detector.fingersUp()
        
        # 3-2. Check distance between landmarks
        x0 , y0  = detector.tipsPosition(0)
        x3 , y3  = detector.tipsPosition(3)
        x4 , y4  = detector.tipsPosition(4)
        x5 , y5  = detector.tipsPosition(5)
        x6 , y6  = detector.tipsPosition(6)
        x8 , y8  = detector.tipsPosition(8)
        x9 , y9  = detector.tipsPosition(9)
        x12, y12 = detector.tipsPosition(12)
        
        xdist_48 = cal_1Ddist(x4, x8)
        xdist_49 = cal_1Ddist(x4, x9)
        xdist_412 = cal_1Ddist(x4, x12)
        xdist_812 = cal_1Ddist(x8, x12)
        ydist_812 = cal_1Ddist(y8, y12)
        dist_412 = cal_2Ddist((x4, y4), (x12, y12))
        dist_812 = cal_2Ddist((x8, y8), (x12, y12))
        xdist_box = bbox[2] - bbox[0] # xmax - xmin
        ydist_box = bbox[3] - bbox[1] # ymax - ymin

        xdist_ratio_48  = xdist_48/xdist_box
        xdist_ratio_49  = xdist_49/xdist_box
        xdist_ratio_412 = xdist_412/xdist_box
        xdist_ratio_812 = xdist_812/xdist_box
        ydist_ratio_812 = ydist_812/ydist_box

        # 3-3. Mode Update
        if    fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1                               :    cMode = NO_MODE
        elif  fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and xdist_ratio_48 >= 0.25                        :    cMode = MOUSE_L_CLICK_WAIT
        elif  fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and xdist_ratio_412 >= 0.87                       :    cMode = MOUSE_DRAG_UP
        elif  fingers[1] == 1 and fingers[2] == 1 and xdist_ratio_49 >= 0.55                                            :    cMode = SCROLL_WAIT
        elif  fingers[1] == 1 and fingers[2] == 1 and xdist_ratio_49 < 0.55                                             :    cMode = SCROLL_MOVE
        elif  fingers[0] == 0 and fingers[1] == 1 and fingers[4] == 1                                                   :    cMode = MOUSE_R_CLICK_WAIT
        elif  xdist_ratio_48 < 0.15 and xdist_ratio_412 < 0.32 and xdist_ratio_812 < 0.32 and ydist_ratio_812 < 0.25    :    cMode = MOUSE_DRAG_DOWN
        elif  fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 0                                                   :    cMode = MIDDLE_FINGER_UP
        elif  fingers[0] == 0 and fingers[1] == 1                                                                       :    cMode = MOUSE_MOVE
       
       # =================== 4. Mouse Operation ================== #
        # 4-1. Cursor is moving
        if cMode == MOUSE_MOVE or cMode == MOUSE_DRAG_DOWN:
            # 1) Check whether mouse cursor is down.
            if pMode != MOUSE_DRAG_DOWN and cMode == MOUSE_DRAG_DOWN:
                ap.mouse.toggle(down=True)
  
            # 2) Get the location of mouse cursor.
            clocX, clocY, cconX, cconY = get_current_location(x0, y0, plocX, plocY, pconX, pconY, fingers_prev)

            # 3) Move mouse cursor.
            ap.mouse.move(W_SCR - clocX, clocY)
            cv.circle(img, (x8, y8), 15, PINK, cv.FILLED)

            # 4) Update the states.
            plocX, plocY = clocX, clocY
            pconX, pconY = cconX, cconY
            fingers_prev = True
            pMode        = cMode

        # 4-2. Left Click
        elif cMode == MOUSE_L_CLICK_WAIT:
            # ap.mouse.toggle(down=False) # (mouse up)
            
            # 1) Find distance between landmarks (58, 56)
            dist_58, img, lineInfo = detector.findDistance(5, 8, img)
            dist_56 = cal_2Ddist((x5, y5), (x6, y6))

            # 2) Click mouse if distance condition is satisfied
            pMode = click_mouse_left(pMode, cMode, img, lineInfo, dist_56/ydist_box, dist_58/ydist_box)
            
            # 3) Update the states.
            fingers_prev = False

        # 4-3. Right Click
        elif cMode == MOUSE_R_CLICK_WAIT:
            ap.mouse.toggle(down=False) # (mouse up)
            
            # 1) Find distance between between landmarks (58, 56)
            dist_58, img, lineInfo = detector.findDistance(5, 8, img)
            dist_56 = cal_2Ddist((x5, y5), (x6, y6))

            # 2) Click mouse if distance condition is satisfied.
            pMode = click_mouse_right(pMode, cMode, img, lineInfo, dist_56/ydist_box, dist_58/ydist_box)
            
            # 3) Update the states.
            fingers_prev = False

        # 4-4. Drag Up
        elif pMode != MOUSE_DRAG_UP and cMode == MOUSE_DRAG_UP:
            # 1) Mouse up.
            ap.mouse.toggle(down=False) 

            # 2) Update the states.
            pMode = cMode

        # 4-5. Wait the Scroll mode.
        elif cMode == SCROLL_WAIT:
            # 1) Get initial position.
            pscroll_x = plocX
            pscroll_y = plocY

            # 2) Update the states.
            pMode = cMode

        # 4-6. Scroll on the screen
        elif pMode == SCROLL_WAIT and cMode == SCROLL_MOVE:
            ap.mouse.toggle(down=False) # (mouse up)

            # 1) Get the location of mouse cursor.
            clocX, clocY, cconX, cconY = get_current_location(x0, y0, plocX, plocY, pconX, pconY, fingers_prev)
            
            # 2) Scroll on the screen.
            if cnt_scroll >= MIN_CNT_SCROLL:
                pg.scroll( int(pscroll_y - clocY) ) # from inital position.
                cnt_scroll = 0
            
            # 3) Update the states.
            cnt_scroll += 1
            plocX, plocY = clocX, clocY
            pconX, pconY = cconX, cconY
            fingers_prev = True

        # 4-7. Middle Finger Up... -> Don't say swear words!!
        elif cMode == MIDDLE_FINGER_UP:
            # 1) Get the bounding box
            xmin, ymin = bbox[0]-30, bbox[1]-30
            xmax, ymax = bbox[2]+30, bbox[3]+30
            if xmin < 1: xmin = 1
            if ymin < 1: ymin = 1
            if xmax > W_SCR : xmax = wCam
            if ymax > H_SCR : ymax = hCam
            
            roi = img[ymin:ymax, xmin:xmax]

            # 2) Blur the bounding box
            roi_blur = cv.blur(roi, (25,25))
            img[ymin:ymax, xmin:xmax] = roi_blur
        
        # 4-8. None
        else:
            ap.mouse.toggle(down=False)
            fingers_prev          = False
            pMode                 = cMode


    # 5. Image Display
    img   = cv.flip(img, 1)             # 1) Flip image
    
    print_mode(cMode, img)              # 2) Print current mode on the image

    pTime = check_show_time(img, pTime) # 3) Frame Rate
    
    cv.imshow("Image", img)             # 4) Display

    # 6. Key Input
    k = cv.waitKey(1) & 0xFF
    if      k == 27:            
        print(" ============= S T O P =============\n")
        break
    elif    k == ord('q'):      
        print(" ------------ P A U S E ------------\n")
        cv.waitKey()

cv.destroyAllWindows()
cap.release()