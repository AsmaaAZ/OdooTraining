from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "a real estate TYPE model "

    name = fields.Char(required = True)