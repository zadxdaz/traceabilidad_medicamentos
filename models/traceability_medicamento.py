from odoo import models, fields, api

class TraceabilityMedicamento(models.Model):
    _name = 'traceability.medicamento'
    _description = 'Trazabilidad de Medicamentos'

    product_id = fields.Many2one('product.product', string='Producto', required=True)
    lot_id = fields.Many2one('stock.production.lot', string='Lote', required=True)
    state = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('procesado', 'Procesado')
    ], string='Estado', default='pendiente', required=True)
    processing_date = fields.Datetime(string='Fecha de Procesamiento')
    processing_id = fields.Char(string='ID de Procesamiento')

    def send_product_trazability(self):
        """Enviar datos del producto al sistema externo y registrar respuesta."""
        for record in self:
            try:
                # Simular envío de datos al sistema externo
                response = self.env['traceability.mock'].send_data({
                    'product_id': record.product_id.id,
                    'lot_id': record.lot_id.id,
                })
                record.processing_id = response.get('processing_id')
                record.processing_date = fields.Datetime.now()
                record.state = 'procesado'
            except Exception as e:
                raise Exception(f"Error al enviar datos: {str(e)}")

    def update_product_trazability_status(self):
        """Actualizar el estado de los productos enviados."""
        for record in self:
            if record.processing_id:
                try:
                    # Simular consulta al sistema externo
                    response = self.env['traceability.mock'].check_status(record.processing_id)
                    record.state = response.get('status', 'pendiente')
                except Exception as e:
                    raise Exception(f"Error al actualizar el estado: {str(e)}")

class TraceabilityLog(models.Model):
    _name = 'traceability.log'
    _description = 'Historial de Envíos de Trazabilidad'

    product_id = fields.Many2one('product.product', string='Producto', required=True)
    send_date = fields.Datetime(string='Fecha de Envío', default=fields.Datetime.now)
    response = fields.Text(string='Respuesta del Sistema Externo')

class TraceabilityMock(models.AbstractModel):
    """Mock del sistema externo para trazabilidad."""
    _name = 'traceability.mock'

    @api.model
    def send_data(self, data):
        """Simular el envío de datos al sistema externo."""
        return {
            'processing_id': '12345',
            'status': 'procesado'
        }

    @api.model
    def check_status(self, processing_id):
        """Simular la verificación de estado en el sistema externo."""
        return {
            'processing_id': processing_id,
            'status': 'procesado'
        }
