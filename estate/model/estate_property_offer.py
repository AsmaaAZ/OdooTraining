from pkgutil import read_code

from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer model"

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'),
                                         ('refused','Refused')],
                              copy = False, )
    partner_id = fields.Many2one('res.partner', required = True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', default = datetime.today())

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = datetime.today() + timedelta(days=record.validity)

    #def _inverse_compute_date_deadline(self):
        #for record in self:
            #record.validity = record.date_deadline - datetime.today()


    def accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
            return True

    def refuse_offer(self):
        for record in self:
            record.status = 'refused'
            return True

    #_sql_constraints = [('price_check', 'CHECK(price >= 0)', 'price must be positive')]

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("PRICE cannot be less than 0")