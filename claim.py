import pyautogui
import time
import captcha
import refresh

def claim(position):
    cross = pyautogui.locateOnScreen(
        'pycho/claim1otracruz.png') or pyautogui.locateOnScreen('pycho/claim2cruz.png')
    if cross is not None:
        pyautogui.click(cross)
    pyautogui.click(position, clicks=2, interval=0.5)
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
            if retry == 10:
                band = True
                refresh.refreshMiner()
                return None
    captchaList = ['pycho2/tiki.png', 'pycho2/headphone.png', 'pycho2/eye.png']
    position = 0
    band = False
    while not band:
        foundPosition = pyautogui.locateOnScreen(captchaList[position])
        if foundPosition is not None:
            if position > 0:
                captcha.captcha()
            elif position == 0:
                pyautogui.click('pycho2/approve.png')
            band = True
        else:
            position = -position + 1
    tout = time.time()
