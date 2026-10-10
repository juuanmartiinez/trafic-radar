def tiempoCoche(intersections):         # tiempo que tarda en cruzar las lineas 0 y 4 del dataset

    assert intersections[0]["measurementLineId"] == 4

    tiempos = []
    for intersection in intersections:
        tiempos.append(intersection["videoTime"])

    linea0 = tiempos[1]
    linea4 = tiempos[0]

    
    return linea4, linea0

def coche_por_id(gt, carId):
    for c in gt["cars"]:
        if c["carId"] == carId:
            return c
    raise ValueError(f"No existe el carId {carId}")