from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'a library book class for library management'

    name = fields.Char(required=True)
    isbn = fields.Char(copy = False)
    author_id = fields.Many2one('library.author', string='Authors', required=True)
    publication_date = fields.Date(default = datetime.today())
    price = fields.Integer(required=True)

    @api.onchange("isbn")
    def _onchange_isbn(self):
        for record in self:
            record_exist = self.env['library.book'].search([('isbn', '=', record.isbn)])
            if record_exist:
                raise UserError("This ISBN already exist")