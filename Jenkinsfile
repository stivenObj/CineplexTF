/*
 * PIPELINE COMPACTO - Caso Cineplanet (P1, P2, P3 en una sola etapa de pruebas)
 * Pega esto en Jenkins: Pipeline → Definition: "Pipeline script" (sin Git)
 *
 * ANTES DE USAR:
 * 1. Reemplaza PYTHON_EXE por la ruta de tu python.exe (obtenida con "where python").
 * 2. Para que el correo se envíe de verdad, configura SMTP en Jenkins:
 *    Manage Jenkins → System → "Extended E-mail Notification" (o "E-mail Notification")
 *    - SMTP server: p.ej. smtp.gmail.com
 *    - Puerto 465/587, usuario y contraseña de aplicación (no la contraseña normal de Gmail)
 *    Sin esa configuración, el paso "mail" fallará (se captura con try/catch abajo
 *    para que no rompa el pipeline).
 */

pipeline {
    agent any

    environment {
        PYTHON_EXE = 'C:\\Users\\StivenOscar\\AppData\\Local\\Python\\bin\\python.exe'
        CORREO_ADMIN = 'equipo-devops@cineplanet-demo.com'
    }

    stages {

        stage('Preparar workspace') {
            steps {
                writeFile file: 'app.py', text: '''import time, random

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
'''

                writeFile file: 'test_pipeline.py', text: '''import time, pytest
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
'''

                writeFile file: 'requirements.txt', text: 'pytest==8.3.3\n'
            }
        }

        stage('Instalar dependencias') {
            steps {
                bat "\"${PYTHON_EXE}\" -m pip install -r requirements.txt"
            }
        }

        stage('Pruebas (P1, P2, P3)') {
            steps {
                bat "\"${PYTHON_EXE}\" -m pytest test_pipeline.py -v"
            }
        }

        stage('Deploy') {
            steps {
                echo 'Pruebas superadas. Desplegando a Producción...'
            }
        }
    }

    post {
        always {
            script {
                def ok = currentBuild.currentResult == 'SUCCESS'
                def asunto = ok ? "Jenkins: Build EXITOSO - ${env.JOB_NAME} #${env.BUILD_NUMBER}"
                                : "Jenkins: Build FALLIDO - ${env.JOB_NAME} #${env.BUILD_NUMBER}"
                def cuerpo = ok ? "Las pruebas P1, P2 y P3 pasaron correctamente. Versión desplegada a Producción."
                                : "Una o más pruebas fallaron. Revisar consola: ${env.BUILD_URL}"
                try {
                    mail to: "${CORREO_ADMIN}", subject: asunto, body: cuerpo
                } catch (Exception e) {
                    echo "No se pudo enviar el correo (¿SMTP configurado en Jenkins?): ${e.message}"
                }
            }
        }
    }
}
