{
    'name': 'dlocal Go 13 Payment Gateway',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Integración de la pasarela de pagos dlocal_go_13',
    'description': """
        Este módulo proporciona una integración de la pasarela de pagos dlocal_go_13 para Odoo.
    """,
    'author': 'Tu nombre o empresa',
    'depends': ['payment'],  # Dependencia de la app de pagos de Odoo
    'data': [
        'views/payment_views.xml',  # Vista para gestionar pagos
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
