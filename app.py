import time, random

class ErrorAsiento(Exception): pass
class ErrorCompra(Exception): pass

HORARIOS = {"AVENGERS_DOOMSDAY": ["14:00", "17:00", "20:00"]}
ASIENTOS = {f"A{i}": {"reservado": False} for i in range(1, 21)}


def consultar_horarios(pelicula):
    return HORARIOS.get(pelicula, [])


def seleccionar_asiento(asiento_id):
    asiento = ASIENTOS.get(asiento_id)
    if asiento is None or asiento["reservado"]:
        raise ErrorAsiento(f"Asiento {asiento_id} no disponible")
    asiento["reservado"] = True
    return True


def confirmar_compra(asiento_id):
    asiento = ASIENTOS.get(asiento_id)
    if not asiento or not asiento["reservado"]:
        raise ErrorCompra(f"No se puede confirmar la compra de {asiento_id}")
    time.sleep(random.uniform(0.01, 0.03))
    return {"asiento": asiento_id, "estado": "CONFIRMADO"}


def reiniciar():
    for a in ASIENTOS.values():
        a["reservado"] = False