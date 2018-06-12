from marshmallow import Schema, fields


class ContactSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Str()
    email = fields.Email()
    phone = fields.Str()


class LineItemSchema(Schema):
    description = fields.Str(required=True)
    quantity = fields.Number(required=True)
    unit_price = fields.Number(required=True)
    total = fields.Method('calculate_total', dump_only=True)

    def calculate_total(self, line_items):
        return 0


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
    subtotal = fields.Method('calculate_subtotal', dump_only=True)
    total = fields.Method('calculate_total', dump_only=True)

    def calculate_subtotal(self, line_items):
        return 0

    def calculate_total(self, line_items):
        return 0
