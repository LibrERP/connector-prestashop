# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2020-2021 Didotech srl
#    (<http://www.didotech.com/>).
#
#    Created on : 2021-03-08
#    Author : Fabio Colognesi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from openerp import models, api


class MrpCorrection(models.Model):
    _name = 'check.mrp.bom'
    _description = 'MRP BoM Check'

    @api.model_cr
    def refresh_table(self):
        """
            Creates views for external Clients.
        """
        cr = self._cr
        logging.debug("Refreshing auxiliar table.")
        cr.execute(
            """
                DROP TABLE IF EXISTS check_bom_template;
                CREATE TABLE check_bom_template AS (
                    SELECT a.product_tmpl_id, a.id AS product_id, b.product_tmpl_id AS mrp_tmpl_id, b.id AS mrp_bom_id FROM product_product a, mrp_bom b WHERE 
                        a.id IN (
                            SELECT product_id FROM mrp_bom
                            )
                        AND b.product_id = a.id
                        AND a.product_tmpl_id != b.product_tmpl_id
                    );
            """
            )
        logging.debug("Refreshing Materialized Views: End.")

    @api.model_cr
    def create_procedure(self):
        """
            Creates views for external Clients.
        """
        cr = self._cr
        cr.execute(
            """
                CREATE OR REPLACE FUNCTION reset_bom_template()
                RETURNS VOID AS
                $BODY$
                DECLARE
                    tblCursor CURSOR  FOR
                            SELECT mrp_bom_id, product_tmpl_id FROM check_bom_template;
                    v_bom_id integer;
                    v_product_tmpl_id integer;
                BEGIN
                  OPEN tblCursor;
                  LOOP
                    FETCH tblCursor INTO v_bom_id, v_product_tmpl_id;
                    EXIT WHEN NOT FOUND;
                    UPDATE mrp_bom SET product_tmpl_id = v_product_tmpl_id WHERE id = v_bom_id;
                  END LOOP;
                  CLOSE tblCursor;
                END;
                $BODY$
                LANGUAGE plpgsql;
            """
            )

    @api.model_cr
    def init(self):
        self.refresh_table()
        self.create_procedure()

    @api.model_cr
    def refresh(self):
        """
            Refreshes BoM product templates (use as scheduled task).
        """
        cr = self._cr
        self.refresh_table()
        cr.execute("SELECT reset_bom_template()")
        logging.debug("Refreshed BoM product templates.")
        return False
