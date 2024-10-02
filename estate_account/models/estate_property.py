import logging

from odoo import models, fields, api, exceptions, Command


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def sold_property(self):
        logging.error(" *** override ***")
        result = super().sold_property()
        values = {
            'partner_id' : self.buyer.id,
            'move_type' : 'out_invoice',
            'invoice_line_ids' : [
              Command.create({
                'name': self.name,
                'quantity': 1,
                'price_unit': self.selling_price,
              }),
              Command.create({
                'name' : 'property sale - 6%',
                'quantity' : 1,
                'price_unit' : self.selling_price * 0.06,
              }),
            Command.create({
                'name': 'administrative fees',
                'quantity': 1,
                'price_unit': 100,
            }),
            ],
        }

        self.env['account.move'].create(values)
        return result