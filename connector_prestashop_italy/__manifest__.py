# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Prestashop Connector Italian localization',
    'version': '12.0.0.4.3',
    'category': 'Connector',
    'depends': [
        'connector_prestashop',
        'l10n_it_fatturapa_in',          # OCA l10n-italy
        'sale_order_type',          # OCA sale-workflow
    ],
    'author': 'Didotech srl',
    'license': 'AGPL-3',

    'data': [
        'views/backend_view.xml',
        'data/scheduled_action.xml',
    ],

    'installable': True
}
