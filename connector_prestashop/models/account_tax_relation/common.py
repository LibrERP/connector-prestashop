# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models
from odoo.addons.component.core import Component


class AccountTaxRelation(models.Model):
    _name = 'account.tax.relation'
    _description = 'Relation between Prestashop and Odoo taxes'

    _order = 'sequence asc'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    prestashop_bind_ids = fields.One2many(
        comodel_name='prestashop.account.tax.relation',
        inverse_name='odoo_id',
        string='PrestaShop Bindings',
        readonly=True
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        index=True,
        string='Company',
    )
    tax_id = fields.Many2one(
        comodel_name='account.tax',
        string='Odoo Tax',
    )


class PrestashopAccountTaxRelation(models.Model):
    _name = 'prestashop.account.tax.relation'
    _inherit = 'prestashop.binding.odoo'
    _inherits = {'account.tax.relation': 'odoo_id'}

    odoo_id = fields.Many2one(
        comodel_name='account.tax.relation',
        string='Tax Relation',
        required=True,
        ondelete='cascade',
        oldname='openerp_id',
    )

    _sql_constraints = [
        ('prestashop_erp_uniq', 'unique(backend_id, odoo_id, prestashop_id)',
         'An ERP record with same ID already exists on PrestaShop.'),
    ]


class TaxRelationAdapter(Component):
    _name = 'prestashop.account.tax.relation.adapter'
    _inherit = 'prestashop.adapter'
    _apply_on = 'prestashop.account.tax.relation'

    _model_name = 'prestashop.account.tax.relation'
    _prestashop_model = 'tax_rule_groups'
