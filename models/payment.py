import requests
from odoo import models, fields, api

class PaymentTransaction(models.Model):
    _name = 'payment.transaction'
    _description = 'Transacción de pago dlocal'

    amount = fields.Float('Cantidad', required=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('done', 'Hecho'),
        ('failed', 'Fallido'),
    ], default='draft', string='Estado')
    payment_method = fields.Selection([
        ('credit_card', 'Tarjeta de Crédito'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Transferencia Bancaria'),
    ], string='Método de pago')

    dlocal_transaction_id = fields.Char('ID Transacción dlocal')

    @api.model
    def create_payment(self, amount, method):
        # Aquí, implementamos la lógica para interactuar con la API de dlocal_go_13
        payment = self.create({
            'amount': amount,
            'payment_method': method,
            'state': 'draft',
        })
        
        # Llamar a la API de dlocal
        response = self.process_payment_with_dlocal(amount, method)
        
        if response and response.get("status") == "success":
            payment.state = "done"
            payment.dlocal_transaction_id = response.get("transaction_id")
        else:
            payment.state = "failed"
        
        return payment

    def process_payment_with_dlocal(self, amount, method):
        # Aquí interactuamos con la API de dlocal_go_13 para procesar el pago.
        url = "https://api.dlocal.com/v1/payments"  # Reemplaza con la URL de la API de dlocal
        headers = {
            "Authorization": "Bearer <API_KEY>",  # Reemplaza con tu API Key de dlocal
        }

        # Aquí asumes que la pasarela de pago necesita estos parámetros (ajústalos según sea necesario)
        data = {
            "amount": amount,
            "currency": "USD",  # O la moneda adecuada
            "method": method,
        }

        # Realizar la solicitud de pago
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
