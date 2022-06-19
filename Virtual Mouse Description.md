.



# AI Virtual Mouse with Hand Gesture Detection

------

**Date:** 2022-06-17

**Author:**  Hee-Yun Kang, Woo-Ju So

**Github:** [hyKangHGU/VirtualMouse](https://github.com/hyKangHGU/VirtualMouse)

**Demo Video:** [AI Virtual Mouse with Hand Gesture Detection](https://www.youtube.com/watch?v=hzf_d3IJKLs)

----------

## 1. Introduction

In this project, we can control the mouse cursor on the monitor by recognizing the hand gesture on the webcam. This shows that you can control your PC by replacing the mouse and touchpad. In addition, the lecturer will be able to take a presentation in front of the camera only by moving their hands. 



**Goal**

The goal of this project is to perform all basic operations of mouse with only hand gestures. The following are basic operations of mouse.

* Left Click
* Right Click
* Double Click
* Drag & Drop
* Scroll



Hand can be recognized by using MediaPipe's hand landmakr model. As shown in the figure below, landmark information for each joint of the hand is available.

![Hand_Landmark](https://user-images.githubusercontent.com/91526930/174493879-430ad4c1-0ea7-4c94-9638-ddfa58cb607c.png)


------------------

## 2. Requirement

### Hardware

- Webcam

  

### Software Installation

- Python 3.7.x or python 3.8.x

- opencv-python

- mediapipe

- autopy

- pyautogui

  

---------------------

## 3. Tutorial Procedure

### Setting up

**Anaconda Install**

[Anaconda - DLIP (gitbook.io)](https://ykkim.gitbook.io/dlip/installation-guide/anaconda)



**Create virtual environment**

Run anaconda prompt in administrator mode.

![Conda_Prompt](https://user-images.githubusercontent.com/91526930/174493890-257c332b-c4a7-4757-ac82-a314b32b350d.png)




Python version == 3.7.13 or 3.8.13 

![create_virtual_mouse_env](https://user-images.githubusercontent.com/91526930/174493907-c1ce096f-c710-41b6-8952-d48540440a55.png)

```
conda create -n virtual_mouse python=3.7.13
conda activate virtual_mouse
```



**Download Files**

[hyKangHGU/VirtualMouse (github.com)](https://github.com/hyKangHGU/VirtualMouse)



**Install Libraries**

```
pip install opencv-python
pip install mediapipe
pip install autopy
pip install pyautogui
```



**Solution for error**

After downloading files and install libraries, you can see execution error. This error means that the protobuf package should be downgraded to 3.20.x.

![Error_1](https://user-images.githubusercontent.com/91526930/174493915-544e7634-2854-4724-b684-52fb73189416.png)

```
pip uninstall protobuf
pip install protobuf==3.20.1
```



### Code Desription

- **VirtualMouse.py :**  Main Program.

- **HandTrackingModule.py :** Class and functions that recognize hands using MediaPipe are defined. (It is referenced by [youtube link](https://www.youtube.com/watch?v=8gPONnGIPgw))

- **Defines.py :** Constant variables related to setting are defined.

- **MouseOperation.py :** Functions related to mouse operation are defined.



The overall flow of the program is in the order of initialization, hand tracking, mode update, mouse operation, and image display. 

#### Initialization

In first step, the necessary modules are imported. Then the webcam and handDetector class are initialized. 'handDetector' class is defined at HandTrackingMoudule.py. The number of hands detected on the webcam is determined by 'maxHands'.

```python
import cv2 as cv
from Defines import *
from MouseOperation import *
from HandTrackingModule import *
import autopy as ap

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = handDetector(maxHands=1)
```



#### Hand Tracking

From here, it is calculated every frame of the webcam. A hand is detected in an image obtained from webcam. Then landmarks and a bounding box of the hand are obtained. And, it is checked whether the landmarks of the hand are detected or not.

```python
# =================== 2. Hand Tracking ================== #
# 2-1. Find hand Landmarks
success, img = cap.read()
img = detector.findHands(img)
lmList, bbox = detector.findPosition(img)

# 2-2. Check the hand detected
if len(lmList) != 0:
```



#### Mode Update

If the hand is detected, the mode is updated. The information on hand landmarks is utilized of mode change. The 'fingers' variable means whether each finger is stretched or folded. For example, fingers[0] = 1 means the thumb is up. The location information of each landmark is obtained through 'tipsPosision' function. It is used for detail condition of  mode change. Some modes may require the distance between landmarks. The location information is used for calculating the distance. The landmark number is described on image in introduction. Therefore, the modes are determined by each finger's state and the distance between landmarks. The flowchart for mode selection is shown in the following figure.

```python
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
if    fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1             :    cMode = NO_MODE
elif  fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and xdist_ratio_48 >= 0.25      :    cMode = MOUSE_L_CLICK_WAIT
elif  fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and xdist_ratio_412 >= 0.87     :    cMode = MOUSE_DRAG_UP
elif  fingers[1] == 1 and fingers[2] == 1 and xdist_ratio_49 >= 0.55                          :    cMode = SCROLL_WAIT
elif  fingers[1] == 1 and fingers[2] == 1 and xdist_ratio_49 < 0.55                           :    cMode = SCROLL_MOVE
elif  fingers[0] == 0 and fingers[1] == 1 and fingers[4] == 1                                 :    cMode = MOUSE_R_CLICK_WAIT
elif  xdist_ratio_48 < 0.15 and xdist_ratio_412 < 0.32 and xdist_ratio_812 < 0.32 and ydist_ratio_812 < 0.25    
																							  :    cMode = MOUSE_DRAG_DOWN
elif  fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 0                                 :    cMode = MIDDLE_FINGER_UP
elif  fingers[0] == 0 and fingers[1] == 1                                                     :    cMode = MOUSE_MOVE
```

![FlowChart](https://user-images.githubusercontent.com/91526930/174493926-49555cb3-73df-4467-b698-096bf85caa09.png)





#### Mouse Operation

- **Mouse cursor moving**



| ![moving_mode](https://user-images.githubusercontent.com/91526930/174493945-6449af66-f704-4314-a559-6c1b8a05f4a4.png) | ![drag_down_mode](https://user-images.githubusercontent.com/91526930/174493965-1847b969-259c-4af3-8c1b-11e6f951b8d9.png) |
| :--------------------------------------: | :--------------------------------------------: |
|               Moving Mode                |                 Drag Down Mode                 |

The mouse cursor can be moved during the pre-click and click-down state. As shown in the figure above, when only the second finger is up, the mouse moves without clicking. On the other hand, drag down mode is performed in click-down state and can move until drop mode is executed with click-up.

```python
# 4-1. Mouse cursor is moving
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
```



- **Left Click**



| ![left_click_wait_mode](https://user-images.githubusercontent.com/91526930/174493977-d78d13da-b971-4066-b1bb-e7c1cfc7d2aa.png) | ![left_click_mode](https://user-images.githubusercontent.com/91526930/174493980-06e4e524-a027-4551-a155-0e52f4ca1c27.png) |
| :--------------------------------------------------------: | :----------------------------------------------: |
|                  Left-Click Standby Mode                   |                 Left-Click Mode                  |

Left-click standby mode stops the mouse movement before executing a left-click. For detecting the left-click mode, the distance condition between each joint of the 2nd finger is used. In addition, if the condition is continuously satisfied, the left-click is also continuously executed. This problem is solved by recording the state in the previous frame through a variable called 'pMode'.

```python
# 4-2. Left Click
elif cMode == MOUSE_L_CLICK_WAIT:
    ap.mouse.toggle(down=False) # (mouse up)

    # 1) Find distance between landmarks (58, 56)
    dist_58, img, lineInfo = detector.findDistance(5, 8, img)
    dist_56 = cal_2Ddist((x5, y5), (x6, y6))

    # 2) Click mouse if distance condition is satisfied
    pMode = click_mouse_left(pMode, cMode, img, lineInfo, dist_56/ydist_box, dist_58/ydist_box)

    # 3) Update the states.
    fingers_prev = False
```



- **Right Click**

| ![right_click_wait_mode](https://user-images.githubusercontent.com/91526930/174494002-f2550458-fa0f-4185-9ccf-b0f1edab0d1c.png) | ![right_click_mode](https://user-images.githubusercontent.com/91526930/174494001-d14a64ef-a929-43cd-a90d-9b9f93f515a1.png) |
| :----------------------------------------------------------: | :------------------------------------------------: |
|                   Right-Click Standby Mode                   |                  Right-Click Mode                  |

The right-click mode is implemented same to the left-click mode except for the shape of the fingers.

```python
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
```



- **Drag Up**

| ![drag_down_mode](https://user-images.githubusercontent.com/91526930/174494043-702b59f1-9b6e-4da4-90eb-8b6539f80b16.png) | ![Drop_mode](https://user-images.githubusercontent.com/91526930/174494046-7521028b-ee92-449f-b04d-a2c79c538581.png) |
| :--------------------------------------------: | :----------------------------------: |
|                 Drag Down Mode                 |             Drag Up Mode             |

Drag-up mode is a function to escape from drag mode. In drag mode, the cursor can be moved in a click-down state, and stopped in a click-up state. Drag-up mode executes a click-up.

```python
# 4-4. Drag Up
elif pMode != MOUSE_DRAG_UP and cMode == MOUSE_DRAG_UP:
    # 1) Mouse up.
    ap.mouse.toggle(down=False) 

    # 2) Update the states.
    pMode = cMode
```



- **Scroll**



| ![scroll_wait_mode](https://user-images.githubusercontent.com/91526930/174494061-50fb6fa3-8765-4abf-b41a-e31c3ee436a1.png) | ![scroll_mode](https://user-images.githubusercontent.com/91526930/174494058-5eaa1b46-9fdd-48c7-b6d0-4712e17106f5.png) |
| :------------------------------------------------: | :--------------------------------------: |
|                Scroll Standby Mode                 |                  Scroll                  |

In the scroll standby state, the current mouse cursor position is saved. And, in the scroll mode, the screen moves as much as the hand moves in the y-axis direction. The scroll speed is difference in the current hand position compared to the saved mouse cursor position in the scroll standby state.

```python
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
```



- **Middle Finger Filter**

![middle_finger_filter_mode](https://user-images.githubusercontent.com/91526930/174494083-7fff8394-659b-4f6d-936b-7ca89b5bdedc.png)


Since someone can offend the other person by swearing with their fingers, blur processing is performed to prevent this. 

```python
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
```



- **None**

![none_mode](https://user-images.githubusercontent.com/91526930/174494093-df3f42c4-4538-4103-981f-d369c2b4e3f5.png)


This is a nothing mode. This is a mode that prevents the mouse from moving and not doing any action. 

```python
# 4-8. None
else:
    ap.mouse.toggle(down=False)
    fingers_prev          = False
    pMode                 = cMode
```



#### Image Display

```python
# 5. Image Display
img   = cv.flip(img, 1)             # 1) Flip image

print_mode(cMode, img)              # 2) Print current mode on the image

pTime = check_show_time(img, pTime) # 3) Frame Rate

cv.imshow("Image", img)             # 4) Display
```



---------------

## 4. Results and Analysis

### CPS Test

CPS means click per second. CPS can be measured in this [website](https://checkcps.com/ko/). We were able to compare the click speed of a general mouse and a virtual mouse. The test counts the number of clicks in 5 seconds. The results for 5 times are as follows.

| ![general_mouse_CPS TEST](https://user-images.githubusercontent.com/91526930/174494108-bd56a852-c8de-4366-94b5-b95a149290f5.png) | ![virtual_mouse CPS Test](https://user-images.githubusercontent.com/91526930/174494109-60c69a49-ccdd-431b-855c-c59bd1bb2ecb.png) |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
|                        General Mouse                         |                        Virtual Mouse                         |

The average CPS of general mouse is 5.56. On the other hand, the average CPS of the virtual mouse is 4.16. This means that the virtual mouse can click at about 75% of the speed of a general mouse. 







### [Mole Game](https://edcoach.tistory.com/entry/꿀멘토두더지게임)

The mole game was developed to practice mouse movements and clicks. Using this game, we compared a general mouse and a virtual mouse. 



![mole game](.\images\mole game.png)

| ![general_mouse mole_game](https://user-images.githubusercontent.com/91526930/174494106-ee3a81c1-dacb-4b58-a35b-c23429aabc39.png) | ![virtual_mouse mole_game](https://user-images.githubusercontent.com/91526930/174494111-338b7db4-4bf4-48f0-8d3f-d75494d8330a.png) |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
|                        General Mouse                         |                        Virtual Mouse                         |

For a general mouse, a maximum score of 609 was obtained, and for a virtual mouse, a maximum of 200 was obtained. It means that the movement and click accuracy of the virtual mouse is about 3 times lower than that of a general mouse.




### Evaluation by Function

- **Left / Right / Double click**

  It works well without any functional problems, and unwanted multiple clicks are prevented.

- **Scroll**

​		It works well, but lowers the FPS

- **Drag & Drop**

​		It works well.




### Further Work

- **Wheel click**

​		A general mouse has a wheel click function. However, that function has not yet been implemented in this project.

- **FPS down problem at Scroll**

​		Although the scroll function is well implemented, there is a problem that the FPS is lowered.

- **Stopping Error**

  Stopping error is generated when top bar of the image  window is clicked by virtual mouse. We haven't tried it, but here's a solution to solve this. The whole program is composed of two main program files as each independent.  One is to control the virtual mouse from image processing. The other thing is to show the image in real time. 

- **Robustness for Each Operation**

  It is implemented to perform specific actions with predefined hand gestures. Even if the gesture is the same in the eyes of a human, it may be recognized as a different gesture. For example, even though it is cursor moving mode, it may be recognized as left click waiting mode according to a change in posture. It should be implemented to minimized the interference between each operation by giving additional conditions. 




  | ![moving_normal](https://user-images.githubusercontent.com/91526930/174494155-3b0d28cc-13ce-43c1-a512-6ed4d71c89a5.png) | ![moving_fault_recognition](https://user-images.githubusercontent.com/91526930/174494153-a2e5d871-d5d2-45ec-8504-58a4aed08eb9.png) | ![left_click_normal](https://user-images.githubusercontent.com/91526930/174494150-c010691a-c0cf-4e77-aa0f-0f9836c3c8f8.png) |
  | :------------------------------------------: | :----------------------------------------------------------: | :--------------------------------------------------: |
  |                 Moving Mode                  |                      Fault Recognition                       |               Left Click Waiting Mode                |

- **Brick Breaker Game**

  Among the games with the mouse movements, there is a brick breaker game. If you link this game with the virtual mouse, it will be interesting content. 

- **Two Hands Recognition**

  More functions can be implemented by recognizing both hands. If the recognition of the two hands movements is further developed, it is possible to create a model that can interpret sign language.

  

-----------------

## 5. References

[Hands - mediapipe (google.github.io)](https://google.github.io/mediapipe/solutions/hands)

[(2) AI Virtual Mouse | OpenCV Python | Computer Vision - YouTube](https://www.youtube.com/watch?v=8gPONnGIPgw)

