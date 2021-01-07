# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PrestashopBackend(models.Model):
    _inherit = 'prestashop.backend'

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
