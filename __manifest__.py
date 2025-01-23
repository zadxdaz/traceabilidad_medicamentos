# -*- coding: utf-8 -*-
{
    'name': 'Trazabilidad de Medicamentos',
    'version': '1.0.0',
    'summary': 'Gestión de trazabilidad para medicamentos integrando compras y ventas con sistemas externos.',
    'description': """
        Este módulo permite gestionar la trazabilidad de medicamentos, integrando
        las operaciones de compras y ventas con un sistema externo mediante una API.
        Incluye la sincronización de productos trazados y el seguimiento del estado de los envíos.
    """,
    'author': 'Pedro Esteban Jabie',
    'website': 'http://www.example.com',
    'category': 'Inventory',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'product',
        'stock',
        'sale',
        'purchase',
    ],
    'data': [
    'views/traceability_medicamento_views.xml',
    'views/stock_picking_traceability_views.xml',
    'views/traceability_medicamento_report_views.xml',
    'views/menu_views.xml',
    'security/ir.model.access.csv',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}
