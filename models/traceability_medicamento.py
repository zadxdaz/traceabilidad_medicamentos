from odoo import models, fields, api

class TraceabilityMedicamento(models.Model):
    _name = 'traceability.medicamento'
    _description = 'Trazabilidad de Medicamentos'

    product_id = fields.Many2one('product.product', string='Producto', required=True)
    lot_id = fields.Many2one('stock.production.lot', string='Lote', required=False)
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
                
    def generate_traceability_report(self):
        """Generar un reporte de trazabilidad en formato PDF."""
        report_data = []
        for record in self.search([]):
            report_data.append({
                'Producto': record.product_id.display_name,
                'Lote': record.lot_id.name if record.lot_id else 'N/A',
                'Estado': record.state,
                'Fecha de Procesamiento': record.processing_date or 'N/A',
                'ID de Procesamiento': record.processing_id or 'N/A',
            })
        return report_data

    def action_export_report(self):
        """Exportar el reporte de trazabilidad a un archivo PDF."""
        report_data = self.generate_traceability_report()
        # Aquí agregarías la lógica para convertir los datos a un PDF usando una librería como reportlab o wkhtmltopdf
        # Por ahora, devolvemos los datos generados como simulación
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/traceability_medicamento/report?download=true',
            'target': 'new',
        }

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


class TraceabilityMedicamentoViews(models.Model):
    _inherit = 'traceability.medicamento'

    def action_send_pending(self):
        """Acción para enviar productos pendientes al sistema externo."""
        for record in self.search([('state', '=', 'pendiente')]):
            record.send_product_trazability()

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_open_traceability(self):
        """Abrir trazabilidad asociada a la entrega/recepción."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Trazabilidad de Medicamentos',
            'res_model': 'traceability.medicamento',
            'view_mode': 'tree,form',
            'domain': [('lot_id', 'in', self.move_line_ids.lot_id.ids)],
            'context': {
                'default_lot_id': self.move_line_ids.lot_id.id if self.move_line_ids else False,
            },
        }

    def button_validate(self):
        """Extender la validación para iniciar la trazabilidad."""
        res = super(StockPicking, self).button_validate()
        for move_line in self.move_line_ids:
            if move_line.product_id.tracking != 'none' and move_line.lot_id:
                self.env['traceability.medicamento'].create({
                    'product_id': move_line.product_id.id,
                    'lot_id': move_line.lot_id.id,
                    'state': 'pendiente',
                })
        return res
