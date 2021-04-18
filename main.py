import pyautogui
import os
import time
import claim

path = 'pycho'
imagesList = os.listdir(path)
tout = time.time()
while True:
    for position in range(len(imagesList)):
        photo = path + '/' + imagesList[position]
        foundPosition = pyautogui.locateOnScreen(photo)
        tin = time.time()
        if foundPosition is not None:
            print(imagesList[position])
            if (imagesList[position] == 'claim2.png' or imagesList[position] == 'claim1.png') and (tin-tout > 2):
                claim.claim(foundPosition)
            elif not (imagesList[position] == 'claim2.png' and imagesList[position] == 'claim1.png'):
                pyautogui.doubleClick(foundPosition)
                pyautogui.moveTo(1, 20)
        else:
            print('-----', foundPosition)
