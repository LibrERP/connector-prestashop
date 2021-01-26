# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)
import datetime


class Currency(models.Model):
    _inherit = 'res.currency'

    @api.multi
    def swap(self, amount, date):
        self.ensure_one()
        rate_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        if rate_date.weekday() in (5, 6):
            rate_date -= datetime.timedelta(days=rate_date.weekday() - 4)

        rate = self.env['res.currency.rate'].search([
            ('currency_id', '=', self.id),
            ('name', '=', rate_date.strftime('%Y-%m-%d'))
        ])
        if rate:
            return float(amount) / rate.rate
        else:
            if rate_date.weekday() == 0:
                rate_date -= datetime.timedelta(days=3)
            else:
                rate_date -= datetime.timedelta(days=1)
            rate = self.env['res.currency.rate'].search([
                ('currency_id', '=', self.id),
                ('name', '=', rate_date.strftime('%Y-%m-%d'))
            ])
            if rate:
                return float(amount) / rate.rate
            else:
                return 0
