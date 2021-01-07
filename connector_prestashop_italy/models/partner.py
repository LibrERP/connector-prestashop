# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.connector.components.mapper import (
    mapping,
    only_create,
)
from odoo.addons.connector_prestashop.models.res_partner.importer import PartnerImportMapper
import re

EUROPEAN_UNION = {
    'AT': 'Austria',
    'BE': 'Belgio',
    'BG': 'Bulgaria',
    'CY': 'Cipro',
    'HR': 'Croazia',
    'DK': 'Danimarca',
    'EE': 'Estonia',
    'FI': 'Finlandia',
    'FR': 'Francia',
    'DE': 'Germania',
    # 'GB': 'Gran Bretagna',
    'EL': 'Grecia',
    'IE': 'Irlanda',
    'IT': 'Italia',
    'LV': 'Lettonia',
    'LT': 'Lituania',
    'LU': 'Lussemburgo',
    'MT': 'Malta',
    'NL': 'Olanda',
    'PL': 'Polonia',
    'PT': 'Portogallo',
    'CZ': 'Repubblica Ceca',
    'SK': 'Repubblica Slovacca',
    'RO': 'Romania',
    'SI': 'Slovenia',
    'ES': 'Spagna',
    'SE': 'Svezia',
    'HU': 'Ungheria'
}


class ItalyPartnerImportMapper(PartnerImportMapper):
    def get_vat(self, values, country):
        vat_number = values['vat_number'].replace('.', '').replace(' ', '')
        if vat_number:
            regexp = re.compile('^[a-zA-Z]{2}')
            if not regexp.match(vat_number):
                vat_number = country.code + vat_number
            vat_country, vat_number = vat_number[:2].lower(), vat_number[2:]
            if self.env['res.partner'].simple_vat_check(vat_country, vat_number):
                return vat_country, vat_number
        return False

    @only_create
    @mapping
    def property_account_position_id(self, record):
        country = False
        adapter = self.component(usage='backend.adapter')
        address_ids = adapter.client.search('addresses', {'filter[id_customer]': record['id']})
        for address_id in address_ids:
            result = adapter.client.get('addresses', address_id)['address']
            binder = self.binder_for('prestashop.res.country')
            country = country or binder.to_internal(result['id_country'], unwrap=True)
            if 'vat_number' in result:
                get_vat = self.get_vat(result, country)
                if get_vat:
                    vat = get_vat
                    break
        else:
            vat = False

        sale_type_id = self.backend_record.sale_order_type_private_id.id
        account_position_id = self.backend_record.account_position_private_id.id
        preferred_pick_location_id = self.backend_record.stock_location_id.id

        if vat:
            if vat[0].upper() == self.env.user.company_id.partner_id.country_id.code.upper():
                account_position_id = self.backend_record.account_position_business_id.id
                sale_type_id = self.backend_record.sale_order_type_business_id.id
            elif vat[0].upper() in EUROPEAN_UNION:
                account_position_id = self.backend_record.account_position_business_eu_id.id
                sale_type_id = self.backend_record.sale_order_type_business_eu_id.id
            else:
                account_position_id = self.backend_record.account_position_business_non_eu_id
                sale_type_id = self.backend_record.sale_order_type_business_non_eu_id.id
            property_account_receivable_id = self.backend_record.account_receivable_business_id.id
        else:
            property_account_receivable_id = self.backend_record.account_receivable_private_id.id
            if country:
                if country.code.upper() == self.env.user.company_id.partner_id.country_id.code.upper():
                    sale_type_id = self.backend_record.sale_order_type_private_id.id
                elif (country.code.upper() in EUROPEAN_UNION):
                    sale_type_id = self.backend_record.sale_order_type_private_eu_id.id
                    account_position_id = self.backend_record.account_position_private_eu_id.id
                elif (country.code.upper() not in EUROPEAN_UNION):
                    sale_type_id = self.backend_record.sale_order_type_private_non_eu_id.id
                    account_position_id = self.backend_record.account_position_private_non_eu_id.id

        if country and country.code.upper() == self.env.user.company_id.partner_id.country_id.code.upper() or not country:
            property_account_payable_id = self.backend_record.account_payable_national_id.id
        else:
            property_account_payable_id = self.backend_record.account_payable_foreign_id.id

        return {
            'property_account_position_id': account_position_id,
            'property_account_receivable_id': property_account_receivable_id,
            'property_account_payable_id': property_account_payable_id,
            'sale_type': sale_type_id,
            'preferred_pick_location_id': preferred_pick_location_id,
        }

    @only_create
    @mapping
    def e_invoice_detail_level(self, record):
        return {
            'e_invoice_detail_level': self.backend_record.partner_e_invoice_detail_level
        }
