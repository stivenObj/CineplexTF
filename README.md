# Cineplanet - Pipeline CI/CD con Jenkins

Simulación del sistema de venta de entradas de Cineplanet, usada para validar
un pipeline de integración y despliegue continuo (CI/CD) con Jenkins.

## Problemática

- **P1:** Lentitud y saturación de la plataforma durante preventas.
- **P2:** Errores en la disponibilidad de asientos por alta concurrencia.
- **P3:** Fallas durante el proceso de compra (pago/confirmación).

## Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `app.py` | Lógica del sistema: consulta de horarios, selección de asientos y confirmación de compra. |
| `test_pipeline.py` | Pruebas automatizadas (una por cada problemática P1, P2, P3). |
| `requirements.txt` | Dependencias del proyecto (pytest). |
| `Jenkinsfile` | Definición del pipeline: pruebas → despliegue → notificación por correo. |

## Cómo ejecutar las pruebas localmente

```bash
pip install -r requirements.txt
pytest test_pipeline.py -v
```

## Pipeline en Jenkins

El `Jenkinsfile` ejecuta automáticamente las pruebas ante cada cambio y
detiene el despliegue si alguna falla (estrategia *Fail Fast*), notificando
al administrador por correo.
