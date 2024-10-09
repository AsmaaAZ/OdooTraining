from odoo import api, models, fields

class SoldWizard(models.TransientModel):
    _name = 'sold.wizard'
    _description = 'a wizard for selling a property'

    selling_price = fields.Float(string = 'selling price')

    def sold_action(self):
        active_id = self.env.context.get('active_id')
        active_model = self.env.context.get('active_model')
        record = self.env[active_model].browse(active_id)

        record.selling_price = self.selling_price
        record.state = 'sold'