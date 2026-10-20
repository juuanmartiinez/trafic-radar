import json
import os

import cv2

from tracking import detectar_clip, lineas_medida
from velocidad import velocidades_clip
from generarsalidas import dibujar_df


def radar(ruta_video, ruta_calibracion, salida_video="radar.mp4", salida_csv="velocidades.csv"):
    
    # calibracion fija de la camara (la camara nunca se mueve para este set)

    with open(ruta_calibracion) as f:
        calib = json.load(f)
    ruta_mascara = os.path.join(os.path.dirname(ruta_calibracion), calib["mascara"])
    mask = cv2.imread(ruta_mascara, cv2.IMREAD_GRAYSCALE)
    assert mask is not None, f"No se encuentra la máscara: {ruta_mascara}"
    ln4, ln0 = lineas_medida(calib["linea4"], calib["linea0"], ancho=mask.shape[1])

    df = detectar_clip(ruta_video, 0, float("inf"), mask)      # deteccion y tracking del clip 

    # velocidades de cada vehiculo en el clip que se trate
    res = velocidades_clip(df, calib["D"], ln4, ln0)
    res.to_csv(salida_csv, index=False)

    # creamos el video solucion con los resultados obtenidos
    velocidades = dict(zip(res["id"], res["velocidad"])) if len(res) else {}
    dibujar_df(ruta_video, 0, float("inf"), df, salida_video, velocidades=velocidades)

    return res
