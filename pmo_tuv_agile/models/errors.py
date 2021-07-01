from odoo import models, fields, api


class Error(models.Model):
    _name = 'project.error'

    _description = 'Error Management for Help Desk'

    name = fields.Char(required=True)
