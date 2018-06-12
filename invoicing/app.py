from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError, pre_load

from invoicing.schemas import InvoiceSchema

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/api/invoice/', methods=['POST'])
def invoice():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    
    data, errors = InvoiceSchema().load(json_data)
    if errors:
        return jsonify(errors), 422

    return jsonify(data)


if __name__ == '__main__':
    app.run()
