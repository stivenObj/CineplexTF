import time, pytest
from app import consultar_horarios, seleccionar_asiento, confirmar_compra, reiniciar, ErrorAsiento, ErrorCompra

@pytest.fixture(autouse=True)
def limpiar():
    reiniciar()
    yield
    reiniciar()


def test_p1_lentitud_y_saturacion():
    """P1: simula 15 usuarios consultando y comprando en simultáneo."""
    inicio = time.time()
    for i in range(1, 16):
        consultar_horarios("AVENGERS_DOOMSDAY")
        seleccionar_asiento(f"A{i}")
        confirmar_compra(f"A{i}")
    duracion = time.time() - inicio
    assert duracion < 3.0, f"Tardó {duracion:.2f}s, supera el límite aceptable"


def test_p2_disponibilidad_de_asientos():
    """P2: un asiento ya reservado no puede volver a reservarse."""
    seleccionar_asiento("A1")
    with pytest.raises(ErrorAsiento):
        seleccionar_asiento("A1")


def test_p3_fallas_en_proceso_de_compra():
    """P3: no se puede confirmar una compra sin reserva previa."""
    with pytest.raises(ErrorCompra):
        confirmar_compra("A2")
    seleccionar_asiento("A2")
    resultado = confirmar_compra("A2")
    assert resultado["estado"] == "CONFIRMADO"