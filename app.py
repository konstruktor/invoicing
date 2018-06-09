from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError, pre_load

app = Flask(__name__)


class ContactSchema(Schema):
    name = fields.Str()
    address = fields.Str()
    email = fields.Email()
    phone = fields.Str()


class LineItemSchema(Schema):
    description = fields.Str()
    quantity = fields.Number()
    unit_price = fields.Number()
    total = fields.Method('calculate_total', dump_only=True)

    def calculate_total(self, line_items):
        return 0


class InvoiceSchema(Schema):
    number = fields.Str()
    issuer = fields.Nested(ContactSchema)
    customer = fields.Nested(ContactSchema)
    date = fields.Date()
    due_date = fields.Date()
    currency = fields.Str()
    tax_percentage = fields.Number()
    line_items = fields.Nested(LineItemSchema, many=True)
    notes = fields.Str()
    subtotal = fields.Method('calculate_subtotal', dump_only=True)
    total = fields.Method('calculate_total', dump_only=True)

    def calculate_subtotal(self, line_items):
        return 0

    def calculate_total(self, line_items):
        return 0


invoice_schema = InvoiceSchema()



@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/api/invoice/', methods=['POST'])
def invoice():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    
    try:
        data = invoice_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    return 'Hello World!'


if __name__ == '__main__':
    app.run()