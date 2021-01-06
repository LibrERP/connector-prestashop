# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Prestashop Connector EU partner',
    'version': '12.0.1.2.1',
    'category': 'Connector',
    'depends': [
        'connector_prestashop',
        'sale_order_type',          # OCA sale-workflow
    ],
    'author': 'Didotech srl',
    'license': 'AGPL-3',

    'data': [
        'views/backend_view.xml'
    ],

    'installable': True
}
