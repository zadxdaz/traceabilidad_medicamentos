from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        """Crear trazabilidad al confirmar la orden."""
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            for line in order.order_line:
                if line.product_id.tracking != 'none':
                    self.env['traceability.medicamento'].create({
                        'product_id': line.product_id.id,
                        'state': 'pendiente',
                    })
        return res