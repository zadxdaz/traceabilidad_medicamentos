from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_open_traceability(self):
        """Abrir la pantalla de trazabilidad para los productos de este picking."""
        self.ensure_one()
        action = self.env.ref('traceability_medicamento.action_traceability_medicamento').read()[0]
        action['domain'] = [('product_id', 'in', self.move_line_ids.product_id.ids)]
        action['context'] = {
            'default_product_id': self.move_line_ids.product_id.id,
            'default_lot_id': False,  # O asigna un valor según el contexto
        }
        return action
