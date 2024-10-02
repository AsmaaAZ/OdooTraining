from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "a real estate model to learn odoo w mahmood"
    _order = "id desc"

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
    state = fields.Selection(selection=[('new','New'),
                                             ('offer_received','Offer Received'),
                                             ('offer_accepted','Offer Accepted'),
                                             ('sold','Sold'),
                                             ('canceled','Canceled')],
                             help='this is the state',
                             copy=False,
                             default='new')

    property_type_id = fields.Many2one('estate.property.type', string = 'Property Type')
    salesperson = fields.Many2one('res.users', string = 'Salesman', default = lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string = 'Buyer')
    tag_ids = fields.Many2many('estate.property.tag', string = 'tags')
    offer_ids = fields.One2many('estate.property.offer','property_id', string = 'offers')

    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute= '_compute_best_price')

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def sold_property(self):
        for record in self:
            if record.state != 'canceled':
                record.state = 'sold'
                return True
            else:
                raise UserError("Canceled Properties Can Not Be Sold")
                return False

    def cancel_property(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
                return True
            else:
                raise UserError("Sold Properties Can not Be Canceled")
                return False

    #_sql_constraints = [('expected_price', 'CHECK(expected_price >= 0)', 'expected price must be positive'),
     #                   ('check_selling_price', 'CHECK(selling_price >= 0)', 'selling price must be positive')]

    @api.constrains('expected_price')
    def _check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("expected cannot be less than 0")

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < record.expected_price * 0.9:
                raise ValidationError("the selling price can't be 90% less than expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink(self):
        if self.state not in ('new', 'canceled'):
            raise UserError(f"you cant delete a property that is {self.state}")
