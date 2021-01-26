# -*- coding: utf-8 -*-
{
    'name': "Connector prestashop currency",

    'summary': """
        Convert order currency in default currency""",

    'description': """
        Convert all prices in default currency.
        This permits to operate without using Multi-Currency in Odoo
    """,

    'author': 'Didotech srl',
    'website': 'https://github.com/LibrERP/connector-prestashop',
    'category': 'Connector',
    'version': '0.1.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'connector_prestashop',
        'currency_rate_update'
    ],

    # always loaded
    'data': [],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
