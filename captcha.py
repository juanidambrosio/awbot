import pyautogui
import speech_recognition as sr
import time
import logger

BACKOFF_MULTIPLIER = 0
logger = logger.getLogger()


def captcha():
    eye = pyautogui.locateOnScreen('pycho2/eye.png')
    if eye is not None:
        return solveCaptcha()
    detected = switchToAudio()
    if detected is True:
        return detected
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
    goBack()
    secondsToSleep = 30 * BACKOFF_MULTIPLIER
    logger.info(
        'Detectaron el bot, esperando %s segundos para tener mejor suerte con el captcha', secondsToSleep)
    time.sleep(secondsToSleep)


def goBack():
    pyautogui.click('pycho2/goBack.png')
    deny = None
    while deny is None:
        deny = pyautogui.locateOnScreen('pycho2/deny.png')
    pyautogui.click(deny)

def switchToAudio():
    headphone = pyautogui.locateOnScreen('pycho2/headphone.png')
    if headphone is not None:
        pyautogui.click(headphone)
        time.sleep(1)
        if pyautogui.locateOnScreen('pycho2/botDetection.png') is not None:
            detectedBot()
            return True


def solveCaptcha():
    listened = listenAudioAndVerify()
    if pyautogui.locateOnScreen('pycho2/botDetection.png'):
        detectedBot()
        return True
    elif listened is False:
        goBack()
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
                audio = None
                try:
                    audio = r.listen(source, timeout=10)
                    logger.info('Escuchado')
                    audioloco = r.recognize_sphinx(audio)
                    pyautogui.click(playbtn[0], playbtn[1] + 70)
                    pyautogui.write(audioloco)
                except sr.WaitTimeoutError as error:
                    logger.info(
                        'No se pudo escuchar el audio, chequea tu configuración de entrada/salida')
                    return False
        else:
            retry += 1
            if retry == 3:
                switchToAudio()
                listenAudioAndVerify()
    pyautogui.click('pycho2/verify.png')
    time.sleep(1)
    pyautogui.move(0, -100)
    return True
    if pyautogui.locateOnScreen('pycho2/multipleSolutions.png') is not None:
        listenAudioAndVerify()
