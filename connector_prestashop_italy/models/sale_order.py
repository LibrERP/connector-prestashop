# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.connector.components.mapper import (
    mapping,
    only_create,
)
from odoo.addons.connector_prestashop.models.sale_order.importer import SaleOrderLineMapper
from odoo.addons.connector_prestashop_italy.models.partner import EUROPEAN_UNION


class ItalySaleOrderLineMapper(SaleOrderLineMapper):

    @mapping
    def tax_id(self, record):
        with self.backend_record.work_on('prestashop.sale.order') as work:
            importer = work.component(usage='record.importer')
            order_record = importer.backend_adapter.read(record['id_order'])

            binder = self.binder_for('prestashop.address')
            address = binder.to_internal(
                order_record['id_address_invoice'] or order_record['id_address_delivery'],
                unwrap=True
            )

        if address.country_id and address.country_id.code in EUROPEAN_UNION:
            return super().tax_id(record)
        elif self.backend_record.tax_extra_eu:
            return {'tax_id': [(6, 0, [self.backend_record.tax_extra_eu.id])]}
        else:
            return super().tax_id(record)
