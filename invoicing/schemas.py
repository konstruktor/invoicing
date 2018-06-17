from decimal import Decimal
from marshmallow import Schema, fields, pre_load


class ContactSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Str()
    email = fields.Email()
    phone = fields.Str()


class LineItemSchema(Schema):
    description = fields.Str(required=True)
    quantity = fields.Number(required=True)
    unit_price = fields.Number(required=True)
    total = fields.Number(required=True)

    @pre_load
    def calculate_total(self, data):
        data['total'] = data['quantity'] * data['unit_price']
        return data


class InvoiceSchema(Schema):
    number = fields.Str(required=True)
    issuer = fields.Nested(ContactSchema, required=True)
    customer = fields.Nested(ContactSchema, required=True)
    date = fields.Date(required=True)
    due_date = fields.Date()
    currency = fields.Str()
    tax_percentage = fields.Number()
    line_items = fields.Nested(LineItemSchema, many=True, required=True)
    notes = fields.Str()
    subtotal = fields.Number()
    total = fields.Number()

    @pre_load
    def calculate_total(self, data):
        data['subtotal'] = Decimal(0)
        for line_item in data['line_items']:
            data['subtotal'] += line_item['quantity'] * line_item['unit_price']
        data['total'] = data['subtotal']
        return data
