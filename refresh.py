import pyautogui

def refreshMiner():
    loading = pyautogui.locateOnScreen(
        'pycho2/loadingTransaction.png')
    if loading is not None:
        pyautogui.click(loading)
        pyautogui.hotkey('alt', 'f4')
        print('se colgo el popup, rippeado')
    refreshed = False
    while not refreshed:
        claiming = pyautogui.locateOnScreen(
            'pycho2/claimingTlm.png') or pyautogui.locateOnScreen('pycho2/claimingTlm2.png')
        if claiming is not None:
            pyautogui.click(claiming)
            pyautogui.press('f5')
            refreshed = True
            print('f5 al minero')
            return None
