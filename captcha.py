import pyautogui
import speech_recognition as sr
import time
import sys

BACKOFF_MULTIPLIER = 0


def captcha():
    global BACKOFF_MULTIPLIER
    headphone = pyautogui.locateOnScreen('pycho2/headphone.png')
    pyautogui.click(headphone)
    time.sleep(1)
    detected = pyautogui.locateOnScreen('pycho2/botDetection.png')
    if detected is not None:
        detectedBot()
    else:
        BACKOFF_MULTIPLIER = 0
        solveCaptcha()


def detectedBot():
    global BACKOFF_MULTIPLIER
    if BACKOFF_MULTIPLIER is not None and BACKOFF_MULTIPLIER != 0:
        BACKOFF_MULTIPLIER += 1
    else:
        BACKOFF_MULTIPLIER = 1
    pyautogui.click('pycho2/goBack.png')
    deny = pyautogui.locateOnScreen('pycho2/deny.png')
    while deny == None:
        deny = pyautogui.locateOnScreen('pycho2/deny.png')
    pyautogui.click(deny, clicks=2, interval=0.5)
    secondsToSleep = int(sys.argv[1]) * BACKOFF_MULTIPLIER
    print('Waiting', secondsToSleep,
            'to have better luck with the captcha')
    time.sleep(secondsToSleep)


def solveCaptcha():
    exce = True
    while exce:
        r = sr.Recognizer()
        mic = sr.Microphone()
        bandst = False
        while not bandst:
            playbtn = pyautogui.locateOnScreen('pycho2/play.png')
            if playbtn is not None:
                bandst = True
        with mic as source:
            pyautogui.doubleClick(playbtn)
            print('pressed')
            audio = r.listen(source)
        print('escuchado')
        audioloco = r.recognize_sphinx(audio)
        pyautogui.click(playbtn[0], playbtn[1] + 70)
        pyautogui.write(audioloco)
        pyautogui.click('pycho2/verify.png')
        time.sleep(1)
        if pyautogui.locateOnScreen('pycho2/multipleSolutions.png') is None:
            exce = False
        approved = False
        while not approved:
            posicion2 = pyautogui.locateOnScreen('pycho2/approve.png')
            redCheckbox = pyautogui.locateOnScreen('pycho2/notARobotRed.png')
            if posicion2 is not None:
                pyautogui.click(posicion2)
                approved = True
            elif redCheckbox is not None:
                pyautogui.click(redCheckbox)
                approved = True
                time.sleep(5)
                captcha()

