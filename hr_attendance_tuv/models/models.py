# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class hr_attendance_tuv(models.Model):
#     _name = 'hr_attendance_tuv.hr_attendance_tuv'
#     _description = 'hr_attendance_tuv.hr_attendance_tuv'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
