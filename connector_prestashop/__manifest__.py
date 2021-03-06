# -*- coding: utf-8 -*-
# Copyright 2011-2013 Camptocamp
# Copyright 2011-2013 Akretion
# Copyright 2015 AvanzOSC
# Copyright 2015-2016 Tecnativa
# Copyright 2020-2021 Didotech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "PrestaShop-Odoo connector",
    "version": "12.0.7.23.20",
    "license": "AGPL-3",
    "depends": [
        "account",
        "base_vat",  # for vat validation on partner address
        "product",
        "product_multi_category",   # oca/product-attribute
        "connector_ecommerce",      # oca/connector-ecommerce
        "base_multi_image",         # https://github.com/LibrERP/connector-prestashop
        "purchase",
        # "product_variant_supplierinfo",  # oca/product-variant
        "stock_available",          # oca/stock-logistics-warehouse
        # TODO: perhaps not needed:
        # "product_variant_cost_price",  # oca/product-variant
    ],
    "external_dependencies": {
        'python': [
            "html2text",
            "prestapyt",      # Manual download and install from https://github.com/prestapyt/prestapyt.git
            # tests dependencies
            "freezegun",
            "vcr",            # Manual install : apt-get install python3-vcr
            "bs4",
        ],
    },
    "author": "Akretion,"
              "Camptocamp,"
              "AvanzOSC,"
              "Tecnativa,"
              "Mind And Go,"
              "Didotech,"
              "Odoo Community Association (OCA)",

    "website": "https://github.com/OCA/connector-prestashop",
    "category": "Connector",
    'demo': [
        'demo/backend.xml',
    ],
    'data': [
        'data/cron.xml',
        'data/product_decimal_precision.xml',
        'data/ecommerce_data.xml',
        'views/prestashop_backend_view.xml',
        'views/product_view.xml',
        'views/product_category_view.xml',
        'views/image_view.xml',
        'views/delivery_view.xml',
        'views/connector_prestashop_menu.xml',
        'views/partner_view.xml',
        'views/sale_view.xml',
        'views/account_view.xml',
        'views/stock_view.xml',
        'security/ir.model.access.csv',
        'security/prestashop_security.xml',
    ],
    'installable': True,
    "application": True,
}
