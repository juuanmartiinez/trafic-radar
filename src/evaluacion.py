def emparejar(t4, gt_validos, tolerancia=0.2):
    mejor = min(gt_validos, key=lambda c: abs(c["intersections"][0]["videoTime"] - t4))
    if abs(mejor["intersections"][0]["videoTime"] - t4) < tolerancia:
        return mejor
    return None

def evaluar(res, gt_validos, tolerancia=0.2):
    parejas = [emparejar(t, gt_validos, tolerancia) for t in res["t4"]]
    res = res.copy()
    res["carId_gt"] = [p["carId"] if p else None for p in parejas]
    res["v_gt"]     = [p["speed"] if p else None for p in parejas]
    res["error"]    = res["velocidad"] - res["v_gt"]
    return res