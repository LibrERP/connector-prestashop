# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PrestashopBackend(models.Model):
    _inherit = 'prestashop.backend'

    # Property_account_position
    account_position_private_id = fields.Many2one(
        comodel_name="account.fiscal.position", string="Private")
    # account_position_private_eu_id = fields.Many2one(
    #   comodel_name="account.fiscal.position", string="Private EU")
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
