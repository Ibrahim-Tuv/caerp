'''
Created on Jan 24, 2019

@author: Zuhair Hammadi
'''
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HolidaysAllocation(models.Model):
    _inherit = "hr.leave.allocation"

    period_date_from = fields.Date('Period Start Date')
    period_date_to = fields.Date('Period End Date')
    
    @api.constrains('period_date_from', 'period_date_to')
    def _check_period_date(self):
        for record in self:
            if record.period_date_from and record.period_date_to and record.period_date_from > record.period_date_to:
                raise ValidationError(_('Period Start Date > Period End Date'))
            if record.period_date_from and not record.period_date_to:
                raise ValidationError(_('Period End Date'))
            if not record.period_date_from and record.period_date_to:
                raise ValidationError(_('Period Start Date'))            