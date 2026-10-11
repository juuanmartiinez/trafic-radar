import cv2

FRAMES_POR_SEGUNDO = 100

def leer_frames(rutaVideo, tInicio, tFinal):
    cap = cv2.VideoCapture(rutaVideo)
    assert cap.isOpened()
    
    frameInicio = round(tInicio * FRAMES_POR_SEGUNDO)
    frameFinal = round(tFinal * FRAMES_POR_SEGUNDO)

    cap.set(cv2.CAP_PROP_POS_FRAMES, frameInicio)

    for i in range(frameInicio, frameFinal):
        ok, frame = cap.read()

        if not ok:
          break

        yield i, i / FRAMES_POR_SEGUNDO, frame

    cap.release()

