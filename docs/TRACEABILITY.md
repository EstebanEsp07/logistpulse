# Trazabilidad — LogistPulse (Sprint 1)

La matriz completa está en el Documento de diseño (PDF). Resumen vigente:

| Historia | Controlador | Servicio | Prueba | PR | Estado |
|----------|-------------|----------|--------|----|--------|
| HU-LP-01 | InventoryController | inventory_service.list_inventory | test_inventory_lists_stock_and_flags_reorder, test_inventory_filter_by_sku | PR-LP-01 | Implementada en esqueleto |
| HU-LP-02 | ReplenishmentController | inventory_service.upsert_rule | test_rule_create_then_update, test_rule_rejects_non_positive_values | PR-LP-02 | Implementada en esqueleto |
| HU-LP-04 | ShipmentController | shipment_service.get_shipment | test_shipment_tracking_found_and_missing | PR-LP-03 | Implementada en esqueleto |
| HU-LP-07 | TelemetryController | telemetry_service.record_reading | test_telemetry_accepts_valid_and_rejects_invalid | PR-LP-04 | Implementada en esqueleto |
| HU-LP-10 | OrderController | order_service.create_order | test_order_reserves_stock_and_blocks_oversell | PR-LP-05 | Implementada en esqueleto |

Actualice las columnas "PR" con el enlace real al fusionar cada Pull Request.
