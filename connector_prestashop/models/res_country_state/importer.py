# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import logging
from odoo.addons.connector.components.mapper import mapping, only_create
from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class CountryStateImporter(Component):
    _name = 'prestashop.res.country.state.importer'
    _inherit = 'prestashop.importer'
    _apply_on = 'prestashop.res.country.state'

    _model_name = ['prestashop.res.country.state']


class DeliveryCarrierBatchImporter(Component):
    """ Import the PrestaShop States/Provinces.
    """
    _name = 'prestashop.res.country.state.batch.importer'
    # _inherit = 'prestashop.delayed.batch.importer'
    _inherit = 'prestashop.direct.batch.importer'
    _apply_on = 'prestashop.res.country.state'

    _model_name = ['prestashop.res.country.state']

    def run(self, filters=None, **kwargs):
        """ Run the synchronization """
        record_ids = self.backend_adapter.search(filters=filters)
        _logger.info('search for prestashop states/provinces %s returned %s',
                     filters, record_ids)
        for record_id in record_ids:
            self._import_record(record_id, **kwargs)


class CarrierImportMapper(Component):
    _name = 'prestashop.res.country.state.import.mapper'
    _inherit = 'prestashop.import.mapper'
    _apply_on = 'prestashop.res.country.state'

    _model_name = 'prestashop.res.country.state'

    direct = [
        ('iso_code', 'code'),
    ]

    @only_create
    @mapping
    def name(self, record):
        return {'name': record['name']}

    @only_create
    @mapping
    def odoo_id(self, record):
        """
        Prevent The duplication of delivery method if id_reference is the same
        Has to be improved
        """

        odoo_state = self.env['res.country.state'].search([
            ('country_id', '=', self.country_id(record)['country_id']),
            ('code', '=', record['iso_code'])
        ])
        _logger.debug("Found state/province %s for reference %s" % (
            odoo_state.name, record['id']
        ))
        if len(odoo_state) == 1:
            return {'odoo_id': odoo_state.id}
        else:
            return {}

    @mapping
    def active(self, record):
        if self.country_id(record)['country_id']:
            return {'active': record['active'] == '1'}
        else:
            return {'active': False}

    @mapping
    def backend_id(self, record):
        return {'backend_id': self.backend_record.id}

    @only_create
    @mapping
    def company_id(self, record):
        return {'company_id': self.backend_record.company_id.id}

    @only_create
    @mapping
    def country_id(self, record):
        binder = self.binder_for('prestashop.res.country')
        country = binder.to_internal(record['id_country'], unwrap=True)
        return {'country_id': country.id}
