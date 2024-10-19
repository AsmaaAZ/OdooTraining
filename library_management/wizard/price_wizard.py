from odoo import api, models, fields

class PriceWizard(models.TransientModel):
    _name = 'price.wizard'
    _description = 'a wizard for to update book prices'

    book_id = fields.One2many('library.book', 'author_ids', string='Book')
    book_ids = fields.Many2many('library.book', string='Books')

    def change_book_price(self):
        active_id = self.env.context.get('active_id')
        active_model = self.env.context.get('active_model')
        record = self.env[active_model].browse(active_id)

        record.book_ids = self.book_ids