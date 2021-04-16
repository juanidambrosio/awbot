import pyautogui
import os
import time
import captcha

camino = 'pycho'
listaDeArc = os.listdir(camino)
tout = time.time()
while True:
    for i in range(len(listaDeArc)):
        foto = camino + '/' + listaDeArc[i]
        posicion = pyautogui.locateOnScreen(foto)
        tin = time.time()
        if posicion is not None:
            print(listaDeArc[i])
            if (listaDeArc[i] == 'claim2.png' or listaDeArc[i] == 'claim1.png') and (tin-tout > 2):
                cross = pyautogui.locateOnScreen(
                    'pycho/claim1otracruz.png') or pyautogui.locateOnScreen('pycho/claim2cruz.png')
                if cross is not None:
                    pyautogui.click(cross)
                pyautogui.doubleClick(posicion)
                band = False
                while not band:
                    cuadra = pyautogui.locateOnScreen(
                        'pycho2/notARobotCheck.png') or pyautogui.locateOnScreen('pycho2/notARobotBlue.png')
                    if cuadra is not None:
                        pyautogui.click(cuadra)
                        pyautogui.moveTo(cuadra[0]-100, cuadra[1]+100)
                        band = True
                    else:
                        hideDetails = pyautogui.locateOnScreen(
                            'pycho2/hideDetails.png')
                        if hideDetails is not None:
                            pyautogui.click(hideDetails)
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
            elif not (listaDeArc[i] == 'claim2.png' and listaDeArc[i] == 'claim1.png'):
                pyautogui.doubleClick(posicion)
                pyautogui.moveTo(1, 20)
        else:
            print('-----', posicion)
