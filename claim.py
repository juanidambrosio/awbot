import pyautogui
import time
import captcha
import refresh
import logger

logger = logger.getLogger()


def claim(foundPosition):
    cross = pyautogui.locateOnScreen(
        'pycho/claim1otracruz.png') or pyautogui.locateOnScreen('pycho/claim2cruz.png')
    if cross is not None:
        pyautogui.click(cross)
    pyautogui.click(foundPosition)
    band = False
    retry = 0
    while not band:
        checkbox = pyautogui.locateOnScreen(
            'pycho2/notARobotCheck.png') or pyautogui.locateOnScreen('pycho2/notARobotBlue.png') or pyautogui.locateOnScreen('pycho2/notARobotRed.png')
        hideDetails = pyautogui.locateOnScreen(
            'pycho2/hideDetails.png')
        if checkbox is not None:
            pyautogui.click(checkbox)
            pyautogui.moveTo(checkbox[0]-100, checkbox[1]+100)
            band = True
        elif hideDetails is not None:
            pyautogui.click(hideDetails)
        else:
            retry += 1
            if retry == 3:
                band = True
                refresh.refreshMiner()
                return None
    captchaList = ['pycho2/tiki.png', 'pycho2/headphone.png',
                   'pycho2/eye.png', 'pycho2/notARobotRed.png']
    position = 0
    retry = 0
    approved = False
    detected = False
    while not approved and not detected and retry < 3:
        foundPosition = pyautogui.locateOnScreen(captchaList[position])
        if foundPosition is not None:
            if position > 0 and position < 3:
                detected = captcha.captcha()
                position = 0
            elif position == 0:
                pyautogui.click('pycho2/approve.png')
                logger.info('Aprobado')
                approved = True
                if pyautogui.locateOnScreen('pycho2/approve.png') is not None:
                    refresh.localizeClaimingTlmAndHitRefresh()
            elif position == 3:
                pyautogui.click('pycho2/notARobotRed.png')
                detected = captcha.captcha()
        elif position < len(captchaList) - 1:
            position += 1
        else:
            position = 0
            retry +=1
    tout = time.time()
