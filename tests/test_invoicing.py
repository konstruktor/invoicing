import pytest
from datetime import date

from invoicing.app import app


def test_invoice_create_success():
    app.config['TESTING'] = True
    client = app.test_client()
    response = client.post('/api/invoice/', json=dict(
        number='1',
        issuer={
            'name': 'Issuer name',
        },
        customer={
            'name': 'Customer name'
        },
        date=str(date.today()),
        line_items=[{
            'description': 'Line item 1',
            'quantity': 2,
            'unit_price': 10
        }]
    ))
    assert response.status_code == 200


def test_invoice_create_validation_error():
    app.config['TESTING'] = True
    client = app.test_client()
    response = client.post('/api/invoice/', json=dict(
        issuer={
            'name': 'Issuer name',
        },
        customer={
            'name': 'Customer name'
        },
        line_items=[{
            'description': 'Line item 1',
            'quantity': 2,
            'unit_price': 10
        }]
    ))
    assert len(response.get_json()) == 2
    assert 'number' in response.get_json()
    assert 'date' in response.get_json()