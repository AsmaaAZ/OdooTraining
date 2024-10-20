from email.policy import default

from odoo import models, fields, api

class LibraryAuthor(models.Model):
    _name = "library.author"
    _description = "a library author class for library management"

    name = fields.Char(required=True)
    birth_date = fields.Date(required = True)
    book_id = fields.One2many('library.book', 'author_ids', string='Book')
    book_ids = fields.Many2many('library.book',string='Books')
    total_books = fields.Integer(compute='_compute_total_books')

    number_of_books_per_author = fields.Integer(default = 0)
    def _compute_total_books(self):
         for record in self:
             if len(self.book_ids) == 0:
                 record.total_books = 0
             else:
                 record.total_books = len(self.book_ids)

    def number_of_books(self):
        for record in self:
            if len(self.book_ids) == 0:
                record.number_of_books_per_author = 0
            else:
                record.number_of_books_per_author = len(self.book_ids)