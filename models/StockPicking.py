from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """Asignar lote a la trazabilidad al validar la recepción."""
        res = super(StockPicking, self).button_validate()
        for move_line in self.move_line_ids:
            if move_line.product_id.tracking != 'none' and move_line.lot_id:
                trazability = self.env['traceability.medicamento'].search([
                    ('product_id', '=', move_line.product_id.id),
                    ('lot_id', '=', False),
                    ('state', '=', 'pendiente'),
                ], limit=1)
                if trazability:
                    trazability.assign_lot(move_line.lot_id.id)
        return res