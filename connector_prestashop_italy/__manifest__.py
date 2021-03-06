# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Prestashop Connector Italian localization',
    'version': '12.0.0.8.0',
    'category': 'Connector',
    'depends': [
        'connector_prestashop',
        'l10n_it_fatturapa_in',     # OCA l10n-italy
        'l10n_it_ddt',              # OCA l10n-italy
        'sale_order_type',          # OCA sale-workflow
    ],
    'author': 'Didotech srl',
    'website': 'https://github.com/LibrERP/connector-prestashop',
    'license': 'AGPL-3',

    'data': [
        'security/ir.model.access.csv',
        'views/backend_view.xml',
        'data/scheduled_action.xml',
    ],

    'installable': True
}
