from videodata import leer_frames
import cv2
from IPython.display import Video, display

COLORES = {2: (0, 255, 0), 3: (255, 0, 255), 5: (0, 165, 255), 7: (0, 0, 255)}  # BGR: coche verde, camión rojo

def dibujar_df(ruta, tInicio, tFinal, df, salida="detecciones.mp4"):
    writer = None
    for idx, t, frame in leer_frames(ruta, tInicio, tFinal):

        for _, f in df[df["frame"] == idx].iterrows():
            x1, y1, x2, y2 = int(f.x1), int(f.y1), int(f.x2), int(f.y2)
            color = COLORES.get(int(f.cls), (255, 255, 255))
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.circle(frame, ((x1 + x2) // 2, y2), 6, color, -1)
            cv2.putText(frame, f"id {int(f.id)} {int(f.cls)} {f.conf:.2f} ", (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        n = (df["frame"] == idx).sum()
        cv2.putText(frame, f"t={t:.2f}s  cajas={n}", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

        if writer is None:
            h, w = frame.shape[:2]
            writer = cv2.VideoWriter(salida, cv2.VideoWriter_fourcc(*"mp4v"), 25, (w, h))
            assert writer.isOpened()
        writer.write(frame)
    writer.release()