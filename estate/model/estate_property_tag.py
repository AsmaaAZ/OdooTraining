from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "a real estate TAGS model "

    name = fields.Char(required = True)

    _sql_constraints = [('check_name', 'UNIQUE(name)', 'a type name must be unique')]