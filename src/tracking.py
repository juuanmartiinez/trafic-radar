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