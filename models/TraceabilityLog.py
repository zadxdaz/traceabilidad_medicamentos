from odoo import models, fields, api


class TraceabilityLog(models.Model):
    _name = 'traceability.log'
    _description = 'Historial de Envíos de Trazabilidad'

    product_id = fields.Many2one('product.product', string='Producto', required=True)
    send_date = fields.Datetime(string='Fecha de Envío', default=fields.Datetime.now)
    response = fields.Text(string='Respuesta del Sistema Externo')
