from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "a real estate TYPE model "
    _order = "name"

    name = fields.Char(required = True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer(string='Sequence', default=1, help="Used to order types")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [('check_type_name', 'UNIQUE(name)', 'a type name must be unique')]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)