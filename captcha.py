import pyautogui
import speech_recognition as sr
import time
import logger

BACKOFF_MULTIPLIER = 0
logger = logger.getLogger()


def captcha():
    eye = pyautogui.locateOnScreen('pycho2/eye.png')
    if eye is not None:
        solveCaptcha()
        return None
    switchToAudio()
    detected = pyautogui.locateOnScreen('pycho2/botDetection.png')
    if detected is not None:
        detectedBot()
        return True
    else:
        global BACKOFF_MULTIPLIER
        BACKOFF_MULTIPLIER = 0
        return solveCaptcha()


def detectedBot():
    global BACKOFF_MULTIPLIER
    if BACKOFF_MULTIPLIER is not None and BACKOFF_MULTIPLIER != 0:
        BACKOFF_MULTIPLIER += 1
    else:
        BACKOFF_MULTIPLIER = 1
    pyautogui.click('pycho2/goBack.png')
    deny = None
    while deny is None:
        deny = pyautogui.locateOnScreen('pycho2/deny.png')
    pyautogui.click(deny, clicks=2, interval=0.5)
    secondsToSleep = 30 * BACKOFF_MULTIPLIER
    logger.info('Detectaron el bot, esperando', secondsToSleep,
                'segundos para tener mejor suerte con el captcha')
    time.sleep(secondsToSleep)


def switchToAudio():
    headphone = pyautogui.locateOnScreen('pycho2/headphone.png') 
    if headphone is not None:
        pyautogui.click(headphone)
        


def solveCaptcha():
    listenAudioAndVerify()
    if pyautogui.locateOnScreen('pycho2/botDetection.png'):
        detectedBot()
        return True
    else:
        return False


def listenAudioAndVerify():
    r = sr.Recognizer()
    mic = sr.Microphone()
    bandst = False
    retry = 0
    while not bandst and retry < 3:
        playbtn = pyautogui.locateOnScreen('pycho2/play.png')
        if playbtn is not None:
            bandst = True
            with mic as source:
                pyautogui.click(playbtn)
                logger.info('Presiono play')
                audio = r.listen(source, timeout=10)
                logger.info('Escuchado')
                audioloco = r.recognize_sphinx(audio)
                pyautogui.click(playbtn[0], playbtn[1] + 70)
                pyautogui.write(audioloco)
        else:
            retry += 1
            if retry == 3:
                switchToAudio()
                listenAudioAndVerify()
    pyautogui.click('pycho2/verify.png')
    time.sleep(1)
    pyautogui.move(0, -100)
    if pyautogui.locateOnScreen('pycho2/multipleSolutions.png') is not None:
        listenAudioAndVerify()
