import pandas as pd
import numpy as np
from videodata import leer_frames
from ultralytics import YOLO

def cajas_de_frame(df, frame):
    return df[df["frame"] == frame][["x1", "y1", "x2", "y2"]].to_numpy()

def iou(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b

    ix1 = max(ax1, bx1)
    iy1 = max(ay1, by1)
    ix2 = min(ax2, bx2)
    iy2 = min(ay2, by2)

    ancho = max(0, ix2 - ix1)
    alto = max(0, iy2 - iy1)

    inter = ancho * alto
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)

    return inter / (area_a + area_b - inter)

def detectar_clip(ruta, tInicio, tFinal, mask, clases=(2, 3, 5, 7)):
    filas = []

    modelo = YOLO("yolo11n.pt")

    for idx, t, frame in leer_frames(ruta, tInicio, tFinal):
        res = modelo.track(frame, persist=True, tracker="bytetrack.yaml",
                   classes=list(clases), verbose=False)[0]
        cajas = res.boxes.xyxy.cpu().numpy()
        confianza = res.boxes.conf.cpu(). numpy()
        clase = res.boxes.cls.cpu().numpy().astype(int)

        if res.boxes.id is None:
            ids = np.full(len(cajas), -1)
        else:
            ids = res.boxes.id.cpu().numpy().astype(int)

        for (x1, y1, x2, y2), conf, cls, tids in zip(cajas, confianza, clase, ids):
            px = min(int((x1 + x2) / 2), mask.shape[1] - 1)
            py = min(int(y2), mask.shape[0] - 1)

            if mask[py, px] > 0:
                filas.append({
                    "frame": idx, "t": t,
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                    "conf": conf, "cls": cls,
                    "id" : tids,
                })

    return pd.DataFrame(filas)