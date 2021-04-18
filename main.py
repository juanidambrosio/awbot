import pyautogui
import os
import time
import claim

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
                claim.claim(posicion)
            elif not (listaDeArc[i] == 'claim2.png' and listaDeArc[i] == 'claim1.png'):
                pyautogui.doubleClick(posicion)
                pyautogui.moveTo(1, 20)
        else:
            print('-----', posicion)
