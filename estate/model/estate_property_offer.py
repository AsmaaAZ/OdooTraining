from pkgutil import read_code

from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

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
    date_deadline = fields.Date(compute='_compute_date_deadline', default = datetime.today(), inverse = '_inverse_compute_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = datetime.today() + timedelta(days=record.validity)

    def _inverse_compute_date_deadline(self):
        for record in self:
            record.validity = record.date_deadline - datetime.today()


    def accept_offer(self):
        for record in self:
            record.status = 'accepted'
            return True

    def refuse_offer(self):
        for record in self:
            record.status = 'refused'
            return True