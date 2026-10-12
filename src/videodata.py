import cv2

def leer_frames(rutaVideo, tInicio, tFinal):
    cap = cv2.VideoCapture(rutaVideo)
    assert cap.isOpened()

    cap.set(cv2.CAP_PROP_POS_MSEC, tInicio * 1000)

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        t = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        if t > tFinal:
            break
        yield round(t * 50), t, frame

    cap.release()

