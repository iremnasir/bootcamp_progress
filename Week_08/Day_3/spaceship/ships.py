import numpy as np
import cv2

img = cv2.imread('./images/background.jpg')
ship = cv2.imread('./images/A13.png')
x = 0
while True:
    frame = img.copy()

    frame[100:100+ship.shape[0], x:x+ship.shape[1]] = ship
    x += 1

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cv2.destroyAllWindows()
