import pyautogui
import logger

logger = logger.getLogger()


def refreshMiner():
    loading = pyautogui.locateOnScreen(
        'pycho2/loadingTransaction.png', confidence=0.8)
    if loading is not None:
        pyautogui.click(loading)
        localizeClaimingTlmAndHitRefresh()
    else:
        logger.info('No se encontró el popup - abortando claim')


def localizeClaimingTlmAndHitRefresh():
    pyautogui.hotkey('alt', 'f4')
    logger.info('Se colgo el popup, rippeado')
    refreshed = False
    retry = 0
    while not refreshed:
        claiming = pyautogui.locateOnScreen(
            'pycho2/claimingTlm.png', confidence=0.8) or pyautogui.locateOnScreen('pycho2/claimingTlm2.png', confidence=0.8)
        if claiming is not None:
            pyautogui.click(claiming)
            pyautogui.press('f5')
            refreshed = True
            logger.info('f5 al minero')
            return None
        else:
            retry += 1
            if retry == 3:
                logger.info(
                    'No se encontró un minero en estado "Claiming TLM", asegurate de recortar bien ambos textos. Tu minero va a quedar inactivo :(')
            return None
