import logging

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'),
                                         ('refused','Refused')],
                              copy = False, )
    partner_id = fields.Many2one('res.partner', required = True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', default = datetime.today())
    property_type_id = fields.Many2one("estate.property.type", string="property type", related="property_id.property_type_id", store=True)

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
            record.property_id.state = 'offer_accepted'
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

    @api.model
    def create(self, vals):
        self.env['estate.property'].browse(vals['property_id']).state = 'offer_received'
        list_prices = []
        max_price = 0

        for i in self.env['estate.property'].browse(vals['property_id']).offer_ids:
            logging.error(i.price)
            list_prices.append(i.price)

        if len(list_prices) >= 1:
            logging.error(" ****** ")
            logging.error(list_prices)
            logging.error(" ****** ")
            max_price = max(list_prices)
            logging.error(max_price)

        logging.error(" ++++ ")
        logging.error(self.env['estate.property'].browse(vals['property_id']).offer_ids.price)
        if self.price <= max_price:
            raise ValidationError("offer has to be higher than other offers")



        return super(EstatePropertyOffer, self).create(vals)