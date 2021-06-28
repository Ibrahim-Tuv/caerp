'''
Created on Nov 4, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields
from dateutil.relativedelta import relativedelta
from datetime import timedelta

class Employee(models.Model):
    _inherit= 'hr.employee'
    
    def get_leave_balance(self, leave_type_id, balance_date = None):
        self.ensure_one()
        if isinstance(leave_type_id, models.BaseModel):
            leave_type_id = leave_type_id.id
        elif isinstance(leave_type_id, int):
            pass
        elif isinstance(leave_type_id, str):
            leave_type_id = self.env['hr.leave.type'].search([('name','=', leave_type_id)], limit = 1).id
            
        if not balance_date:
            balance_date = fields.Date.today()
                
        def duration(date1, date2):
            date1 = fields.Date.from_string(date1)
            date2 = fields.Date.from_string(date2)
            return (date2 - date1).days + 1
        
        balance = 0
        leaves = self.env['hr.leave'].search([('employee_id','=', self.id), ('state', '=', 'validate'), ('holiday_status_id', '=', leave_type_id), ('date_from', '<=', balance_date)])
        for leave in leaves:
            if leave.date_to <= balance_date:
                balance += leave.number_of_days
            else:
                holiday_days = duration(leave.date_from, leave.date_to)
                affected_days = duration(leave.date_from, balance_date)
                balance += leave.number_of_days * (affected_days / holiday_days)
                    
        allocations = self.env['hr.leave.allocation'].search([('employee_id','=', self.id), ('state', '=', 'validate'), ('holiday_status_id', '=', leave_type_id), '|', ('period_date_from', '<=', balance_date), ('period_date_from', '=', False)])
        for allocation in allocations:
            if not allocation.period_date_to or allocation.period_date_to <= balance_date or allocation.accrual:
                balance += allocation.number_of_days
            else:
                from_string = fields.Date.from_string
                to_months = lambda delta : delta.years * 12 + delta.months + delta.days / 30
                holiday_delta = relativedelta(from_string(allocation.period_date_to) + timedelta(days=1), from_string(allocation.period_date_from))
                affected_delta = relativedelta(from_string(balance_date)  + timedelta(days=1), from_string(allocation.period_date_from))
                balance += allocation.number_of_days * (to_months(affected_delta) / to_months(holiday_delta))
                                    
        return round(balance, 2)