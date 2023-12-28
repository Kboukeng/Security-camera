import cv2
import pygame

cam = cv2.VideoCapture(0)
pygame.mixer.init()

while cam.isOpened():
    ret, frame1 = cam.read()
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)  # Convert to grayscale
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        X, Y, W, H = cv2.boundingRect(c)
        cv2.rectangle(frame1, (X, Y), (X+W, Y+H), (0, 255, 0), 1)
        sound = pygame.mixer.Sound('alert.wav')
        sound.play()
    
    if cv2.waitKey(10) == ord('x'):
        break
    cv2.imshow('Security camera', frame1)