from odoo import models, fields, api


class Ticket(models.Model):
    _name = 'project.ticket'

    _description = 'Tickets Management for Help Desk'

    error_id = fields.Many2one('project.error', string='Error Type', required=True)
    description = fields.Text(String="Issue Details")
    status = fields.Selection([('new', 'New'), ('closed', 'Closed'), ('solved', 'Solved')], string="status",
                              default='new')

    def set_ticket_to_closed(self):
        self.status = 'closed'

    def set_ticket_to_solved(self):
        self.status = 'solved'
