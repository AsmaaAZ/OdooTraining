from email.policy import default

from odoo import models, fields
from datetime import datetime, timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "a real estate model to learn odoo w mahmood"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, default = datetime.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Type',
        selection=[('north', 'North'),
                   ('south', 'South'),
                   ('east','East'),
                   ('west','West')], help="Type for garden ori idk what that is")
    active = fields.Boolean(default = True)
    state = fields.Selection(string='Type', selction=[('new','New'),
                                             ('offer_received','Offer Received'),
                                             ('offer_accepted','Offer Accepted'),
                                             ('sold','Sold'),
                                             ('canceled','Canceled')], help='this is the state', copy=False,default='new')