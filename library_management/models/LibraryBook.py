from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import UserError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'a library book class for library management'

    name = fields.Char(required=True)
    isbn = fields.Char(required=True, copy = False)
    author_id = fields.One2many('library.author', 'book_ids',string='Authors', required=True)
    author_ids = fields.Many2many('library.author',string='books', required=True)
    publication_date = fields.Date(default = fields.Date.today)
    price = fields.Integer(required=True)

    number_of_author_per_book = fields.Integer()
    show_number = fields.Boolean(default = False)

    @api.onchange("isbn")
    def _onchange_isbn(self):
        for record in self:
            record_exist = self.env['library.book'].search([('isbn', '=', record.isbn)])
            if record_exist:
                raise UserError("This ISBN already exist")

    def number_of_authors(self):
        for record in self:
            record.show_number = False
            if len(self.author_ids) == 0:
                record.number_of_author_per_book = 0
            else:
                record.show_number = True
                record.number_of_author_per_book = len(self.author_ids)
