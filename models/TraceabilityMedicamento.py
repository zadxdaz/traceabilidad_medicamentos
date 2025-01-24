from odoo import models, fields, api

class TraceabilityMedicamento(models.Model):
    _name = 'traceability.medicamento'
    _description = 'Trazabilidad de Medicamentos'

    product_id = fields.Many2one('product.product', string='Producto', required=True)
    lot_id = fields.Many2one('stock.lot',string='Lote',required=False,
    help="Lote relacionado con el producto para la trazabilidad. Puede ser asignado después de la creación.")

    state = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('procesado', 'Procesado')
    ], string='Estado', default='pendiente', required=True)
    processing_date = fields.Datetime(string='Fecha de Procesamiento')
    processing_id = fields.Char(string='ID de Procesamiento')



    def assign_lot(self, lot_id):
        """Asignar un lote a la trazabilidad."""
        for record in self:
            if record.state == 'pendiente':
                record.lot_id = lot_id
            else:
                raise Exception("No se puede asignar un lote a un registro ya procesado.")

    def send_product_trazability(self):
        """Enviar datos del producto al sistema externo y registrar respuesta."""
        for record in self:
            if not record.lot_id:
                raise Exception(f"El registro de trazabilidad para el producto {record.product_id.name} no tiene un lote asignado.")
            
            try:
                # Simular envío de datos al sistema externo
                response = self.env['traceability.api.mock'].send_data({
                    'product_id': record.product_id.id,
                    'lot_id': record.lot_id.id,
                })
                # Actualizar los campos con la respuesta del sistema externo
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
                    response = self.env['traceability.api.mock'].check_status(record.processing_id)
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

class TraceabilityMedicamentoViews(models.Model):
    _inherit = 'traceability.medicamento'

    def action_send_pending(self):
        """Acción para enviar productos pendientes al sistema externo."""
        for record in self.search([('state', '=', 'pendiente')]):
            record.send_product_trazability()


