import pyautogui
import os
import time
import claim
import logger

path = 'pycho'
imagesList = os.listdir(path)
tout = time.time()
logger = logger.getLogger()
while True:
    for position in range(len(imagesList)):
        photo = path + '/' + imagesList[position]
        foundPosition = pyautogui.locateOnScreen(photo, confidence=0.8)
        tin = time.time()
        if foundPosition is not None:
            logger.info(imagesList[position])
            if (imagesList[position] == 'claim2.png' or imagesList[position] == 'claim1.png') and (tin-tout > 2):
                claim.claim(foundPosition)
            elif not (imagesList[position] == 'claim2.png' and imagesList[position] == 'claim1.png'):
                pyautogui.click(foundPosition)
                pyautogui.moveTo(1, 20)
        else:
            print('-----', foundPosition)
