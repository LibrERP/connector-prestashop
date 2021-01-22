# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
import vatnumber
import logging

_logger = logging.getLogger(__name__)


class PrestashopBackend(models.Model):
    _inherit = 'prestashop.backend'

    # Property_account_position
    account_position_private_id = fields.Many2one(
        comodel_name="account.fiscal.position", string="Private")
    account_position_business_id = fields.Many2one(
        comodel_name="account.fiscal.position", string="Business")
    account_position_private_eu_id = fields.Many2one(
        comodel_name="account.fiscal.position", string="Private EU")
    account_position_business_eu_id = fields.Many2one(
        comodel_name="account.fiscal.position", string="Business EU")
    account_position_private_non_eu_id = fields.Many2one(
        comodel_name="account.fiscal.position", string="Private not EU")
    account_position_business_non_eu_id = fields.Many2one(
        comodel_name="account.fiscal.position", string="Business not EU")

    account_receivable_private_id = fields.Many2one(
        comodel_name="account.account", string="Private")
    account_receivable_business_id = fields.Many2one(
        comodel_name="account.account", string="Business")
    account_payable_national_id = fields.Many2one(
        comodel_name="account.account", string="National")
    account_payable_foreign_id = fields.Many2one(
        comodel_name="account.account", string="Foreign")

    sale_order_type_private_id = fields.Many2one(
        comodel_name="sale.order.type", string="Private")
    sale_order_type_business_id = fields.Many2one(
        comodel_name="sale.order.type", string="Business")
    sale_order_type_private_eu_id = fields.Many2one(
        comodel_name="sale.order.type", string="Private EU")
    sale_order_type_business_eu_id = fields.Many2one(
        comodel_name="sale.order.type", string="Business EU")
    sale_order_type_private_non_eu_id = fields.Many2one(
        comodel_name="sale.order.type", string="Private not EU")
    sale_order_type_business_non_eu_id = fields.Many2one(
        comodel_name="sale.order.type", string="Business not EU")

    partner_e_invoice_detail_level = fields.Selection([
        ('0', 'Minimum'),
        ('1', 'Tax Rate'),
        ('2', 'Maximum'),
    ], string="E-bills Detail Level",
        help="Minimum level: Bill is created with no lines; "
             "User will have to create them, according to what specified in "
             "the electronic bill.\n"
             "Tax rate level: Rate level: an invoice line is created for each "
             "rate present in the electronic invoice\n"
             "Maximum level: every line contained in the electronic bill "
             "will create a line in the bill.",
        default='2', required=True
    )

    tax_extra_eu = fields.Many2one(
        comodel_name="account.tax",
        string="Default extra EU tax",
        required=False,
        help="This tax will be used for all orders outside EU"
    )

    # def button_verify_vat(self):
    #     counter = 0
    #     partner_model = self.env['res.partner']
    #     for partner in partner_model.search([]):
    #         if partner.vat:
    #             vat = partner.vat.replace(' ', '').replace('.', '')
    #             country_code, vat_number = vat[:2], vat[2:]
    #
    #             if not partner_model.simple_vat_check(country_code, vat_number):
    #                 counter += 1
    #                 _logger.debug('{}: {}: "{}"'.format(counter, partner.name, partner.vat))
    #                 # partner.vat = False

    @api.model
    def check_sale_orders(self, domain=None):
        self.search(domain or []).import_customers_since()
        self.search(domain or []).import_sale_orders()

    @api.model
    def update_stock_qty(self, domain=None):
        self.search(domain or []).update_product_stock_qty()
