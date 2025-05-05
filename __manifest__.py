{
    'name': 'dlocal Go 13 Payment Gateway',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Integración de la pasarela de pagos dlocal_go_13',
    'description': """
        Este módulo proporciona una integración de la pasarela de pagos dlocal_go_13 para Odoo.
    """,
    'author': 'Lorenzo Romero',
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',  # Vista para gestionar pagos
        'data/payment_data.xml',    # Datos de configuración (si los tienes)
    ],
    'license': 'LGPL-3',  # Añadir la clave 'license'
    'installable': True,
    'application': True,
    'auto_install': False,
}
