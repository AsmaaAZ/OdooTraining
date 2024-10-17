from odoo import models, fields, api
from datetime import datetime

class LibraryReservations(models.Model):
    _name = "library.reservations"
    _description = "a library reservation class for library management"

    book_id = fields.Many2one('library.book', string = "Book Name")
    date_from = fields.Date()
    borrowing_period = fields.Integer(compute= '_compute_borrow_period', readonly = True)
    return_date = fields.Date(default = fields.Date.today, readonly = True)
    partner_id = fields.Many2one('res.partner', string = 'Partner')
    price = fields.Integer(compute= '_compute_total_price')

    @api.depends('book_id')
    def _compute_total_price(self):
        for record in self:
                record.price = 0

    @api.depends('date_from', 'return_date')
    def _compute_borrow_period(self):
        for record in self:
            fmt = '%Y-%m-%d'
            d1 = datetime.strptime(record.date_from, fmt)
            d2 = datetime.strptime(record.return_date, fmt)
            record.borrowing_period = (d2 - d1).days