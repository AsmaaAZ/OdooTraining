from odoo import models, fields, api
from datetime import datetime

class LibraryReservations(models.Model):
    _name = "library.reservations"
    _description = "a library reservation class for library management"

    book_id = fields.One2many('library.book', 'reservation_ids', string='book', required=True)
    book_ids = fields.Many2many('library.book', string='books', required=True)

    date_from = fields.Date(default = datetime.today())
    borrowing_period = fields.Integer(compute= '_compute_borrow_period', readonly = True)
    return_date = fields.Date(default = datetime.today())
    partner_id = fields.Many2one('res.partner', string = 'Partner')
    price = fields.Integer(compute= '_compute_total_price')

    @api.depends('book_ids')
    def _compute_total_price(self):
        for record in self:
            if len(self.book_ids) == 0:
                record.price = 0
            else:
                for book in record.book_ids:
                    record.price += book.price

    @api.depends('date_from', 'return_date')
    def _compute_borrow_period(self):
        for record in self:
            record.borrowing_period = (record.return_date - record.date_from).days