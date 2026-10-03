# LogistPulse

Plataforma de gestión de pedidos y logística (dominio operativo) del proyecto integrador. Este repositorio contiene el **esqueleto ejecutable del Sprint 1** (SPR-LP-01): arquitectura MVC, base de datos PostgreSQL y entorno Docker.

## 1. Propósito y alcance

LogistPulse da visibilidad al inventario, los envíos, la telemetría y los pedidos de una operación logística. Épicas del producto:

1. Consulta y Reglas de Reposición de Inventario (Smart Inventory)
2. Rastreo Monitoreado de Suministros y Distribución (Supply & Distribution)
3. Monitoreo de Telemetría y Gestión de Incidentes Operativos (Smart Operations)
4. Procesamiento y Gestión de Ciclo de Vida de Pedidos (Order Fulfillment)

**Incluido en el Sprint 1 (esqueleto):** HU-LP-01, HU-LP-02, HU-LP-04, HU-LP-07, HU-LP-10.
**Fuera de alcance:** generación automática de incidentes (HU-LP-08), ciclo de incidentes (HU-LP-09), transiciones del pedido (HU-LP-11/12), integración con GPS o sensores reales, autenticación.

## 2. Stack y versiones

| Componente | Versión |
|------------|---------|
| Python | 3.12 |
| Flask / Flask-SQLAlchemy / SQLAlchemy | 3.1 / 3.1 / 2.0 |
| PostgreSQL | 16 (alpine) |
| Gunicorn | 23 |
| Docker Engine / Compose | 24+ / v2 |

## 3. Requisitos previos

- Git y Docker con Docker Compose v2 (Docker Desktop o GitHub Codespaces).
- Puerto libre `8001` (configurable con `APP_PORT`; distinto de BankPulse para poder correr ambos a la vez).

## 4. Configuración de variables

```bash
cp .env.example .env      # Windows PowerShell: Copy-Item .env.example .env
```

**No suba `.env` al repositorio.**

| Variable | Descripción | Valor de ejemplo |
|----------|-------------|------------------|
| POSTGRES_USER / POSTGRES_PASSWORD / POSTGRES_DB | Credenciales y nombre de la BD | logistpulse / change_me_locally / logistpulse |
| SECRET_KEY | Clave de Flask | change_me_locally |
| APP_PORT | Puerto publicado en el host | 8001 |
| SEED_DATA | Carga datos semilla ficticios | true |
| DB_CONNECT_RETRIES / DB_CONNECT_DELAY | Reintentos y espera (s) hasta que la BD responda | 15 / 2 |

## 5. Comandos

```bash
docker compose up --build -d     # construir e iniciar
docker compose ps                # estado (db y app en healthy)
docker compose logs -f app       # logs de la aplicación
docker compose down              # detener (conserva datos)
docker compose down -v           # detener y borrar el volumen de la BD
```

| Servicio | Puerto host | Notas |
|----------|-------------|-------|
| app (SVC-LP-01) | 8001 | API y vista HTML en http://localhost:8001 |
| db (SVC-LP-02) | no publicado | PostgreSQL solo dentro de la red de Compose; datos en `logistpulse_pgdata` |

## 6. Endpoint de salud y operación demostrable

```bash
curl http://localhost:8001/health
# {"db":"up","service":"logistpulse","status":"ok"}

# HU-LP-01: existencias de la bodega 1 (SKU-002 aparece bajo el punto de reorden)
curl "http://localhost:8001/api/inventory?warehouse_id=1"

# HU-LP-02: configurar regla de reposición
curl -X PUT http://localhost:8001/api/replenishment-rules -H "Content-Type: application/json" \
  -d '{"warehouse_id":2,"product_id":3,"reorder_point":30,"reorder_qty":80}'

# HU-LP-04: rastrear un envío
curl http://localhost:8001/api/shipments/LP-0001

# HU-LP-07: registrar telemetría
curl -X POST http://localhost:8001/api/telemetry -H "Content-Type: application/json" \
  -d '{"device_id":"TRK-01","metric":"temperature","value":4.5,"unit":"C"}'

# HU-LP-10: crear pedido (valida y reserva stock)
curl -X POST http://localhost:8001/api/orders -H "Content-Type: application/json" \
  -d '{"customer_name":"Tienda Demo","warehouse_id":1,"lines":[{"product_id":1,"quantity":20}]}'
```

## 7. Pruebas

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q          # usa SQLite en memoria; no requiere Docker
```

## 8. Estructura de carpetas

```
logistpulse/
├── README.md
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore / .dockerignore
├── requirements.txt
├── wsgi.py
├── .github/
│   └── pull_request_template.md
├── app/
│   ├── __init__.py              # create_app (Application Factory) + espera de la BD
│   ├── config.py
│   ├── extensions.py
│   ├── seed.py
│   ├── models/                  # MODELO: inventory, shipment, telemetry, order
│   ├── views/                   # VISTA: templates/home.html, presenters.py
│   ├── controllers/             # CONTROLADOR: un Blueprint por recurso
│   └── services/                # Reglas de negocio y errores de dominio
├── tests/
│   ├── conftest.py
│   └── test_api.py
└── docs/
    ├── ARCHITECTURE.md
    ├── BRANCHING.md
    ├── TRACEABILITY.md
    └── evidence/
```

## 9. Arquitectura y flujo de trabajo

- Arquitectura MVC: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- Estrategia de ramas (GitHub Flow): [docs/BRANCHING.md](docs/BRANCHING.md)
- Trazabilidad: [docs/TRACEABILITY.md](docs/TRACEABILITY.md)

## 10. Solución de problemas frecuentes

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| `variable is not set` al ejecutar compose | Falta `.env` | `cp .env.example .env` |
| `port is already allocated` | Puerto 8001 ocupado | Cambie `APP_PORT` y repita `docker compose up -d` |
| La app no conecta a la BD al inicio | La BD aún arranca | Normal unos segundos; revise `docker compose logs app` |
| Falla el login a PostgreSQL tras cambiar credenciales | El volumen conserva las anteriores | `docker compose down -v` y levante de nuevo |
| En Codespaces no abre localhost:8001 | Puerto no reenviado | Pestaña *Ports* → puerto 8001 |
