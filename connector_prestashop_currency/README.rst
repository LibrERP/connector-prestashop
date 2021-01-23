
Description
===========

Convert all prices in default currency.
This permits to operate without using different currencies in Odoo, though Multi-Currency should be enabled and you should enable currencies from which the conversion should be done.


Installation
============

This module requires module currency_rate_update:

    https://github.com/OCA/currency/tree/12.0/currency_rate_update

To enable scheduled currency rates update:

  # Go to Invoicing > Configuration > Settings # Ensure Automatic Currency Rates (OCA) is checked

To configure currency rates providers:

  # Go to Invoicing > Configuration > Currency Rates Providers # Create and configure one or more providers

To update historical currency rates:

  # Go to Invoicing > Configuration > Currency Rates Providers # Select specific providers # Launch Actions > Update Rates Wizard # Configure date interval and click Update


Contributors
------------

* Andrei Levin <andrei.levin@didotech.com>
