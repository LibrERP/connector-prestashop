# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.connector.components.mapper import (
    mapping,
    only_create,
)
from odoo.addons.connector_prestashop.models.sale_order.importer import SaleOrderImportMapper


class CurrencySaleOrderImportMapper(SaleOrderImportMapper):
    _inherit = 'prestashop.sale.order.mapper'
    _apply_on = 'prestashop.sale.order'

    @mapping
    def order_currency_id(self, record):
        binder = self.binder_for('prestashop.res.currency')
        currency = binder.to_internal(record['id_currency'], unwrap=True)
        return {'order_currency_id': currency.id}
