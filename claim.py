import pyautogui
import time
import captcha
import refresh

def claim(foundPosition):
    cross = pyautogui.locateOnScreen(
        'pycho/claim1otracruz.png') or pyautogui.locateOnScreen('pycho/claim2cruz.png')
    if cross is not None:
        pyautogui.click(cross)
    pyautogui.click(foundPosition, clicks=2, interval=0.5)
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
            if retry == 5:
                band = True
                refresh.refreshMiner()
                return None
    captchaList = ['pycho2/tiki.png', 'pycho2/headphone.png', 'pycho2/eye.png', 'pycho2/notARobotRed.png']
    position = 0
    retry = 0
    approved = False
    detected = False
    while not approved and not detected:
        foundPosition = pyautogui.locateOnScreen(captchaList[position])
        if foundPosition is not None:
            if position > 0 and position < 3:
                detected = captcha.captcha()
            elif position == 0:
                pyautogui.click('pycho2/approve.png')
                print('Aprobado')
                approved = True
                if pyautogui.locateOnScreen('pycho2/approve.png') is not None:
                    refresh.localizeClaimingTlmAndHitRefresh()
            elif position == 3:
                pyautogui.click('pycho2/notARobotRed.png')
                detected = captcha.captcha()
        else:
            if position < len(captchaList) - 1:
                position += 1
            else:
                position = 0
    tout = time.time()
