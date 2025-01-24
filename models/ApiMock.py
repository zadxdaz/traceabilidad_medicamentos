from odoo import models, fields, api

class TraceabilityApiMock(models.AbstractModel):
    """Mock del sistema externo para trazabilidad."""
    _name = 'traceability.api.mock'

    @api.model
    def send_data(self, data):
        """Simular el envío de datos al sistema externo."""
        return {
            'processing_id': '12345',
            'status': 'en camino'
        }

    @api.model
    def check_status(self, processing_id):
        """Simular la verificación de estado en el sistema externo."""
        return {
            'processing_id': processing_id,
            'status': 'en camino'
        }
