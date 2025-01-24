from odoo import models, fields

class TraceabilityConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_url = fields.Char(
        string='URL de la API',
        config_parameter='traceability_medicamento.api_url',
        default='https://api.external-system.com'
    )
    use_mock_api = fields.Boolean(
        string='Usar Mock API Integrada',
        config_parameter='traceability_medicamento.use_mock_api',
        default=True
    )
