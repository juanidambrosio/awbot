import pyautogui
import time
import captcha


def claim(posicion):
    cross = pyautogui.locateOnScreen(
        'pycho/claim1otracruz.png') or pyautogui.locateOnScreen('pycho/claim2cruz.png')
    if cross is not None:
        pyautogui.click(cross)
    pyautogui.doubleClick(posicion)
    band = False
    retry = 0
    while not band:
        cuadra = pyautogui.locateOnScreen(
            'pycho2/notARobotCheck.png') or pyautogui.locateOnScreen('pycho2/notARobotBlue.png')
        hideDetails = pyautogui.locateOnScreen(
            'pycho2/hideDetails.png')
        if cuadra is not None:
            pyautogui.click(cuadra)
            pyautogui.moveTo(cuadra[0]-100, cuadra[1]+100)
            band = True
        elif hideDetails is not None:
            pyautogui.click(hideDetails)
        else:
            retry += 1
            if retry == 10:
                pyautogui.click('pycho2/loadingTransaction.png')
                pyautogui.hotkey('alt', 'f4')
                refreshed = False
                while not refreshed:
                    claiming = pyautogui.locateOnScreen('pycho2/claimingTlm.png')
                    if claiming is not None:
                        pyautogui.click('pycho2/claimingTlm.png')
                        pyautogui.press('f5')
                        refreshed = True
                return None
    listita = ['pycho2/tiki.png', 'pycho2/headphone.png']
    i = 0
    band = False
    while not band:
        posicion1 = pyautogui.locateOnScreen(listita[i])
        if posicion1 is not None:
            if i == 1:
                captcha.captcha()
            elif i == 0:
                pyautogui.click('pycho2/approve.png')
            band = True
        else:
            i = -i + 1
    tout = time.time()
