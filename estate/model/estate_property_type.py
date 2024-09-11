from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "a real estate TYPE model "

    name = fields.Char(required = True)

    _sql_constraints = [('check_type_name', 'UNIQUE(name)', 'a type name must be unique')]