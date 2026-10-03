# Arquitectura MVC — LogistPulse

```
Cliente (navegador / sistema externo)
        │  1. Solicitud HTTP            ▲ 6. Respuesta (HTML o JSON)
        ▼                               │
VISTA        views/templates/home.html · views/presenters.py
        │                               ▲
CONTROLADOR  controllers/*_controller.py (Blueprints Flask)
        │                               ▲
SERVICIOS    services/*_service.py (reglas de negocio)
        │                               ▲
MODELO       models/*.py (SQLAlchemy) ──► PostgreSQL 16 (volumen logistpulse_pgdata)
```

| Capa | Elementos | Responsabilidad |
|------|-----------|-----------------|
| Modelo | Warehouse, Product, StockLevel, ReplenishmentRule, Shipment, TrackingEvent, TelemetryReading, Order, OrderLine | Entidades y persistencia |
| Vista | home.html, presenters (inventory_view, rule_view, shipment_view, telemetry_view, order_view) | Representación de la respuesta |
| Controlador | HealthController, InventoryController, ReplenishmentController, ShipmentController, TelemetryController, OrderController | Recibir la petición, validar entrada, invocar servicios y elegir la vista |
| Servicios | inventory_service, shipment_service, telemetry_service, order_service | Reglas de negocio (stock disponible, reposición, validación de lecturas) |

Patrones: Application Factory, Blueprint por controlador, capa de servicios, presentadores.
El diagrama completo y la justificación están en el Documento de diseño (PDF).
