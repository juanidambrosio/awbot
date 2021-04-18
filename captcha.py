import pyautogui
import speech_recognition as sr
import time
import sys

BACKOFF_MULTIPLIER = 0


def captcha():
    eye = pyautogui.locateOnScreen('pycho2/eye.png')
    if eye is not None:
        solveCaptcha()
        return None
    headphone = pyautogui.locateOnScreen('pycho2/headphone.png')
    pyautogui.click(headphone)
    time.sleep(1)
    detected = pyautogui.locateOnScreen('pycho2/botDetection.png')
    if detected is not None:
        detectedBot()
    else:
        global BACKOFF_MULTIPLIER
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
    secondsToSleep = 30 * BACKOFF_MULTIPLIER
    print('Detectaron el bot, esperando', secondsToSleep,
          'segundos para tener mejor suerte con el captcha')
    time.sleep(secondsToSleep)


def solveCaptcha():
    listenAudioAndVerify()
    if pyautogui.locateOnScreen('pycho2/botDetection.png'):
        detectedBot()
        return None
    approved = False
    retry = 0
    while not approved and retry < 10:
        approveButton = pyautogui.locateOnScreen('pycho2/approve.png')
        redCheckbox = pyautogui.locateOnScreen('pycho2/notARobotRed.png')
        if approveButton is not None:
            pyautogui.click(approveButton)
            print('Aprobado')
            approved = True
        elif redCheckbox is not None:
            pyautogui.click(redCheckbox)
            print('Check rojo apretado')
            approved = True
            captcha()
        retry += 1
    if retry == 10:
        pyautogui.hotkey('alt', 'f4')


def listenAudioAndVerify():
    r = sr.Recognizer()
    mic = sr.Microphone()
    bandst = False
    while not bandst:
        playbtn = pyautogui.locateOnScreen('pycho2/play.png')
        if playbtn is not None:
            bandst = True
            with mic as source:
                pyautogui.click(playbtn)
                print('Presiono play')
                audio = r.listen(source, timeout=10)
                print('Escuchado')
                audioloco = r.recognize_sphinx(audio)
                pyautogui.click(playbtn[0], playbtn[1] + 70)
                pyautogui.write(audioloco)
    pyautogui.click('pycho2/verify.png')
    time.sleep(1)
    pyautogui.move(0, -100)
    if pyautogui.locateOnScreen('pycho2/multipleSolutions.png') is not None:
        listenAudioAndVerify()
