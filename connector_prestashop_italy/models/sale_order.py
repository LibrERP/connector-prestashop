# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.connector.components.mapper import (
    mapping,
    only_create,
)
from odoo.addons.connector_prestashop.models.sale_order.importer import SaleOrderLineMapper
from odoo.addons.connector_prestashop.models.sale_order.importer import SaleOrderImportMapper
from odoo.addons.connector_prestashop_italy.models.partner import EUROPEAN_UNION


class ItalySaleOrderImportMapper(SaleOrderImportMapper):
    _inherit = 'prestashop.sale.order.mapper'
    _apply_on = 'prestashop.sale.order'

    @mapping
    def fiscal_position_id(self, record):
        partner_data = self.partner_invoice_id(record)
        partner = self.env['res.partner'].browse(partner_data['partner_invoice_id'])

        sale_type_id = self.backend_record.sale_order_type_private_id.id
        account_position_id = self.backend_record.account_position_private_id.id

        if partner.country_id:
            if partner.vat:
                if partner.country_id.code.upper() == self.env.user.company_id.partner_id.country_id.code.upper():
                    account_position_id = self.backend_record.account_position_business_id.id
                    sale_type_id = self.backend_record.sale_order_type_business_id.id
                elif partner.country_id.code.upper() in EUROPEAN_UNION:
                    account_position_id = self.backend_record.account_position_business_eu_id.id
                    sale_type_id = self.backend_record.sale_order_type_business_eu_id.id
                else:
                    account_position_id = self.backend_record.account_position_business_non_eu_id.id
                    sale_type_id = self.backend_record.sale_order_type_business_non_eu_id.id
            else:
                if partner.country_id.code.upper() == self.env.user.company_id.partner_id.country_id.code.upper():
                    sale_type_id = self.backend_record.sale_order_type_private_id.id
                    account_position_id = self.backend_record.account_position_private_id.id
                elif partner.country_id.code.upper() in EUROPEAN_UNION:
                    sale_type_id = self.backend_record.sale_order_type_private_eu_id.id
                    account_position_id = self.backend_record.account_position_private_eu_id.id
                elif partner.country_id.code.upper() not in EUROPEAN_UNION:
                    sale_type_id = self.backend_record.sale_order_type_private_non_eu_id.id
                    account_position_id = self.backend_record.account_position_private_non_eu_id.id

        print(partner.name)
        print(account_position_id)
        print(sale_type_id)

        return {
            'fiscal_position_id': account_position_id,
            'type_id': sale_type_id
        }


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
