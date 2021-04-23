import pyautogui
import time
import captcha
import refresh
import logger

logger = logger.getLogger()


def claim(foundPosition):
    previousChecks()
    pyautogui.click(foundPosition)
    band = False
    retry = 0
    while not band:
        checkbox = pyautogui.locateOnScreen(
            'pycho2/notARobotCheck.png', confidence=0.8)
        if checkbox is not None:
            pyautogui.click(checkbox)
            band = True
        else:
            retry += 1
            if retry == 100:
                band = True
                refresh.refreshMiner()
                return None
    captchaList = ['pycho2/tiki.png', 'pycho2/headphone.png',
                   'pycho2/eye.png', 'pycho2/notARobotRed.png']
    position = 0
    approved = False
    detected = False
    while not approved and not detected:
        foundPosition = pyautogui.locateOnScreen(captchaList[position], confidence=0.8)
        if foundPosition is not None:
            if position > 0 and position < 3:
                detected = captcha.captcha()
                position = 0
            elif position == 0:
                pyautogui.click('pycho2/approve.png')
                pyautogui.move(0, -100)
                logger.info('Aprobado')
                global BACKOFF_MULTIPLIER
                BACKOFF_MULTIPLIER = 0
                approved = True
            elif position == 3:
                pyautogui.click('pycho2/notARobotRed.png', confidence=0.8)
                detected = captcha.captcha()
        elif position < len(captchaList) - 1:
            position += 1
        else:
            position = 0
    tout = time.time()


def previousChecks():
    cross = pyautogui.locateOnScreen(
        'pycho/claim1otracruz.png', confidence=0.8) or pyautogui.locateOnScreen('pycho/claim2cruz.png', confidence=0.8)
    if cross is not None:
        pyautogui.click(cross)
    deny = pyautogui.locateOnScreen('pycho/deny.png', confidence=0.8)
    if deny is not None:
        pyautogui.click(deny)
