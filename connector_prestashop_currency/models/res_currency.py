# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import openerp.addons.decimal_precision as dp
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)
import datetime

class Currency(models.Model):
    _inherit = 'res.currency'

    @api.multi
    def swap(self, amount, date):
        self.ensure_one()
        rate = self.env['res.currency.rate'].search([
            ('currency_id', '=', self.id),
            ('name', '=', date)
        ])
        if rate:
            return float(amount) / rate.rate
        else:
            order_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', self.id),
                ('name', '=', (order_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
            ])
            if rate:
                return float(amount) / rate.rate
            else:
                return 0
