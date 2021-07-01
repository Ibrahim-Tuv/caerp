from odoo import models, fields


class Release(models.Model):
    _name = 'project.release'

    _description = 'Project  Agile Relaease Management'

    name = fields.Char()
    description = fields.Text()
    date = fields.Date()
    project_id = fields.Many2one('project.project', String='Project')


class Backlogs(models.Model):
    _name = 'project.backlog'

    _description = 'Project Agile Backlogs Management'

    name = fields.Char()
    assigned_date = fields.Date(string="Assigned Date", required=True)
    deadline = fields.Date(string="Deadline")
    assigned_by = fields.Many2one('hr.employee', String='Empolyee')
    project_id = fields.Many2one('project.project', String='Project')
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
