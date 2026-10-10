import cv2
import pandas as pd


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

def detectar_clip(ruta, tInicio, tFinal, modelo, mask, clases=(2, 3, 5, 7)):
    filas = []
    for idx, t, frame in leer_frames(ruta, tInicio, tFinal):
        res = modelo(frame, classes=list(clases), verbose=False)[0]
        cajas = res.boxes.xyxy.cpu().numpy()
        confianza = res.boxes.conf.cpu(). numpy()
        clase = res.boxes.cls.cpu().numpy().astype(int)

        for (x1, y1, x2, y2), conf, cls in zip(cajas, confianza, clase):
            px = min(int((x1 + x2) / 2), mask.shape[1] - 1)
            py = min(int(y2), mask.shape[0] - 1)

            if mask[py, px] > 0:
                filas.append({
                    "frame": idx, "t": t,
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                    "conf": conf, "cls": cls,
                })

    return pd.DataFrame(filas)