import requests
from odoo import models, fields, api

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'  # Heredamos el modelo payment.transaction de Odoo
    _description = 'Transacción de pago dlocal'

    # Agregamos un nuevo campo para el método de pago
    payment_method = fields.Selection([
        ('credit_card', 'Tarjeta de Crédito'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Transferencia Bancaria'),
    ], string='Método de pago')

    # Agregamos un campo para almacenar el ID de la transacción de dlocal
    dlocal_transaction_id = fields.Char('ID Transacción dlocal')

    @api.model
    def create_payment(self, amount, method):
        # Creamos una nueva transacción de pago en estado "draft"
        payment = self.create({
            'amount': amount,
            'payment_method': method,
            'state': 'draft',  # Estado inicial
        })

        # Llamamos a la API de dlocal para procesar el pago
        response = self.process_payment_with_dlocal(amount, method)

        # Verificamos la respuesta de la API de dlocal
        if response and response.get("status") == "success":
            payment.state = "done"
            payment.dlocal_transaction_id = response.get("transaction_id")
        else:
            payment.state = "failed"
        
        return payment

    def process_payment_with_dlocal(self, amount, method):
        # URL de la API de dlocal (reemplazar con la URL real si es diferente)
        url = "https://api.dlocal.com/v1/payments"
        
        # Agrega tu clave de API de dlocal aquí
        headers = {
            "Authorization": "Bearer <API_KEY>",  # Reemplaza con tu API key
        }

        # Aquí definimos los parámetros de la solicitud (ajustar según la API de dlocal)
        data = {
            "amount": amount,
            "currency": "USD",  # Puedes cambiar la moneda si es necesario
            "method": method,  # 'credit_card', 'paypal', 'bank_transfer', etc.
        }

        # Realizamos la solicitud POST a la API de dlocal
        try:
            response = requests.post(url, json=data, headers=headers)
            # Verificamos si la respuesta es exitosa (código 200)
            if response.status_code == 200:
                return response.json()  # Retorna la respuesta de la API como un diccionario
            else:
                # Si la respuesta no es exitosa, devolvemos None
                return None
        except Exception as e:
            # Si ocurre un error en la conexión, lo registramos
            _logger.error("Error al procesar el pago con dlocal: %s", e)
            return None
            
    def confirm_payment(self):
        """Método para confirmar el pago manualmente desde la interfaz"""
        if self.state != 'done':
            # Llamamos a la API de dlocal para procesar el pago
            response = self.process_payment_with_dlocal(self.amount, self.payment_method)
            
            # Verificamos la respuesta de la API de dlocal
            if response and response.get("status") == "success":
                self.state = "done"
                self.dlocal_transaction_id = response.get("transaction_id")
                return {'type': 'ir.actions.client', 'tag': 'reload'}
            else:
                self.state = "failed"
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Error',
                        'message': 'No se pudo procesar el pago',
                        'type': 'danger',
                    }
                }
        return {'type': 'ir.actions.client', 'tag': 'reload'}
