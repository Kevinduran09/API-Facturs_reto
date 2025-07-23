from tortoise.models import Model
from tortoise import fields

class Factura(Model):
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=50)
    reference_code = fields.CharField(max_length=100)
    total = fields.CharField(max_length=50)
    customer_name = fields.CharField(max_length=255)
    