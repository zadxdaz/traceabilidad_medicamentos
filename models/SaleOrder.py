from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """Crear trazabilidad al confirmar la orden."""
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                if line.product_id.tracking != 'none':
                    self.env['traceability.medicamento'].create({
                        'product_id': line.product_id.id,
                        'state': 'pendiente',
                    })
        return res