# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    original_total_amount = fields.Monetary(string='Total Amount', readonly=True)
    original_total_amount_tax = fields.Monetary(string='Taxes', readonly=True)


class PrestashopSaleOrder(models.Model):
    _inherit = 'prestashop.sale.order'

    def create(self, data):
        if 'order_currency_id' in data and 'pricelist_id' in data:
            pricelist = self.env['product.pricelist'].browse(data['pricelist_id'])
            if data['order_currency_id'] != pricelist.currency_id.id:
                # convert to default currency
                client_currency = self.env['res.currency'].browse(data['order_currency_id'])

                data.update({
                    'original_total_amount': data['total_amount'],
                    'original_total_amount_tax': data['total_amount_tax'],
                    'total_amount': client_currency.swap(data['total_amount'], data['date_order']),
                    'total_amount_tax': client_currency.swap(
                        data['total_amount_tax'], data['date_order']
                    ),
                    'total_shipping_tax_included': client_currency.swap(
                        data['total_shipping_tax_included'], data['date_order']
                    ),
                    'total_shipping_tax_excluded': client_currency.swap(
                        data['total_shipping_tax_excluded'], data['date_order']
                    )
                })

                for line in data['prestashop_order_line_ids']:
                    line[2]['price_unit'] = client_currency.swap(
                        line[2]['price_unit'], data['date_order']
                    )

        return super().create(data)


# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     def create(self, data):
#         return super().create(data)
#
#     def write(self, data):
#         return super().write(data)
