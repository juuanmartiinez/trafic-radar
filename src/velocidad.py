import numpy as np
import pandas as pd

def tiempo_entre_lineas(tray, ln4, ln0):

    t4 = t0 = None

    primera = tray.iloc[0]
    if primera.y2 >= ln4[int((primera.x1 + primera.x2) / 2)]:
        return None

    for fila in tray.itertuples():
        x = int((fila.x1 + fila.x2) / 2)

        if t4 is None and fila.y2 >= ln4[x]:
            t4 = fila.t
        if t0 is None and fila.y2 >= ln0[x]:
            t0 = fila.t

    if t4 is None or t0 is None:
        return None

    return (t0, t4)

def calibrar_distancia(gt, t_max=1200):
    distancias = []
    for c in gt["cars"]:
        if c["valid"] and len(c["intersections"]) == 2 and c["intersections"][1]["videoTime"] < t_max:
            dt = c["intersections"][1]["videoTime"] - c["intersections"][0]["videoTime"]
            distancias.append(c["speed"] / 3.6 * dt)
    return np.median(distancias)

def velocidades_clip(df, D, ln4, ln0):
    resultados = []

    for coche, tray in df[df["id"] >= 0].groupby("id"):
        tray = tray.sort_values("frame")
        cruces = tiempo_entre_lineas(tray, ln4, ln0)

        if cruces is None:
            continue

        t0, t4 = cruces
        tiempo = t0 - t4

        if tiempo > 0:
            resultados.append({"id": coche, "t4": t4, "tiempo": tiempo, "velocidad": D / tiempo * 3.6})

    return pd.DataFrame(resultados)
