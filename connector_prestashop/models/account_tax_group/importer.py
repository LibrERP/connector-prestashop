# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.addons.connector.components.mapper import (
    mapping,
    only_create,
)
from odoo.addons.component.core import Component


class TaxGroupMapper(Component):
    _name = 'prestashop.account.tax.group.import.mapper'
    _inherit = 'prestashop.import.mapper'
    _apply_on = 'prestashop.account.tax.group'

    _model_name = 'prestashop.account.tax.group'

    direct = [
        ('name', 'name'),
    ]

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @mapping
    def company_id(self, record):
        return {'company_id': self.backend_record.company_id.id}

    @only_create
    @mapping
    def odoo_id(self, record):
        # 'account.tax.group'
        tax_group = self.model.odoo_id.with_context(lang='en_EN').search([
            ('name', '=', record['name'])
        ], order='id', limit=1)
        if tax_group:
            # already_binded = self.check_binding(record, tax_group.id)
            # if already_binded:
            #     return {
            #         'name': already_binded['new_name']
            #     }
            # else:
            return {
                'odoo_id': tax_group.id
            }

    # def check_binding(self, record, odoo_id):
    #     counter = 1
    #     while odoo_id and self.model.search([
    #         ('odoo_id', '=', odoo_id),
    #         ('backend_id', '=', self.backend_record.id)
    #     ]):
    #         counter += 1
    #         name = '{} {}'.format(record['name'], counter)
    #         odoo = self.model.odoo_id.with_context(lang='en_EN').search([
    #             ('name', '=', name)
    #         ], limit=1)
    #         odoo_id = odoo and odoo.id or False
    #
    #     if counter == 1:
    #         return False
    #     else:
    #         return {'new_name': name}


class TaxGroupImporter(Component):
    _name = 'prestashop.account.tax.group.importer'
    _inherit = 'prestashop.importer'
    _apply_on = 'prestashop.account.tax.group'

#     _model_name = 'prestashop.account.tax.group'


class TaxGroupBatchImporter(Component):
    _name = 'prestashop.account.tax.group.direct.batch.importer'
    _inherit = 'prestashop.direct.batch.importer'
    _apply_on = 'prestashop.account.tax.group'

#     _model_name = 'prestashop.account.tax.group'
