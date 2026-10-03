from ..services.errors import DomainError


def register_controllers(app):
    from .health_controller import bp as health_bp
    from .inventory_controller import bp as inventory_bp
    from .order_controller import bp as order_bp
    from .replenishment_controller import bp as replenishment_bp
    from .shipment_controller import bp as shipment_bp
    from .telemetry_controller import bp as telemetry_bp

    for bp in (health_bp, inventory_bp, replenishment_bp, shipment_bp, telemetry_bp, order_bp):
        app.register_blueprint(bp)

    @app.errorhandler(DomainError)
    def handle_domain_error(err):
        return {"error": err.message}, err.status
