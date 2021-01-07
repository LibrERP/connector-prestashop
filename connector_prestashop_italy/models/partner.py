# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.connector.components.mapper import (
    mapping,
    only_create,
)
from odoo.addons.connector_prestashop.models.res_partner.importer import PartnerImportMapper


class ItalyPartnerImportMapper(PartnerImportMapper):
    @only_create
    @mapping
    def e_invoice_detail_level(self, record):
        return {
            'e_invoice_detail_level': self.backend_record.partner_e_invoice_detail_level
        }
