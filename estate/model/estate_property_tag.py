from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "a real estate TAGS model "

    name = fields.Char(required = True)