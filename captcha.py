import pyautogui
import speech_recognition as sr
import time
import logger

BACKOFF_MULTIPLIER = 0
logger = logger.getLogger()


def captcha():
    eye = pyautogui.locateOnScreen('pycho2/eye.png', confidence=0.8)
    if eye is not None:
        return solveCaptcha()
    detected = switchToAudio()
    if detected is True:
        return detected
    else:
        global BACKOFF_MULTIPLIER
        BACKOFF_MULTIPLIER = 0
        return solveCaptcha()


def solveCaptcha():
    listened = listenAudioAndVerify()
    detected = pyautogui.locateOnScreen('pycho2/botDetection.png', confidence=0.8)
    if detected is not None:
        detectedBot()
        return True
    elif listened is False:
        goBack()
        return True
    else:
        return False


def switchToAudio():
    headphone = pyautogui.locateOnScreen('pycho2/headphone.png', confidence=0.8)
    if headphone is not None:
        pyautogui.click(headphone)
        time.sleep(2)
        detected = pyautogui.locateOnScreen('pycho2/botDetection.png', confidence=0.8)
        if detected is not None:
            detectedBot()
            return True


def listenAudioAndVerify():
    r = sr.Recognizer()
    mic = sr.Microphone()
    bandst = False
    retry = 0
    while bandst is not True and retry < 2:
        playbtn = pyautogui.locateOnScreen('pycho2/play.png', confidence=0.8)
        if playbtn is not None:
            bandst = True
            listened = playAudioAndWrite(r, mic, playbtn)
            if listened is False:
                return False
        else:
            retry += 1
            if retry == 2:
                return None
    time.sleep(2)
    multipleSolutions = pyautogui.locateOnScreen('pycho2/multipleSolutions.png', confidence=0.8)
    if multipleSolutions is not None:
        logger.info('Reintento de audio')
        playbtn = pyautogui.locateOnScreen('pycho2/play.png', confidence=0.8)
        return playAudioAndWrite(r, mic, playbtn)


def playAudioAndWrite(r, mic, playbtn):
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
            pyautogui.click('pycho2/verify.png')
            pyautogui.move(0, -100)
            return True
        except sr.WaitTimeoutError as error:
            logger.info(
                'No se pudo escuchar el audio, chequea tu configuración de entrada/salida')
            return False


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
        deny = pyautogui.locateOnScreen('pycho/deny.png')
    time.sleep(1)
    pyautogui.click(deny)
