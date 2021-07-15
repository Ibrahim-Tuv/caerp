# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-Today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
import time
from datetime import date,datetime 
import calendar
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from datetime import date, datetime, time ,timedelta
from calendar import weekday, monthrange, SUNDAY,SATURDAY

class RepairReport(models.AbstractModel):
    _name = 'report.abs_monthly_attendance_report.single_manager_report'
    _description = "Maintenance summary"

    #Get employee report value function
    def _get_report_values(self, docids, data=None):
        manager_ids = []
        employee_ids = []
        doc_model = []
        docs = []
        month = []
        if docids:
            employee_ids = self.env['hr.employee'].search([('parent_id', 'in', docids)])
            if employee_ids:
                for employee in employee_ids:
                    manager = employee.parent_id.name
                    now = datetime.now()
                    year = now.year
                    month = now.month - 1
                    month_date=date(int(now.year),int(month),1)
                    date_from=month_date.replace(day=1)
                    date_to=month_date.replace(day=calendar.monthrange(month_date.year,month_date.month)[1])
                    start_date = date_from.strftime("%m/%d/%Y")
                    end_date = date_to.strftime("%m/%d/%Y")
                    today = date_from
                    day=date(int(now.year), int(month) ,1)
                    single_day = timedelta(days=1)
                    weekday = month
                    days = 0
                    while day.month == today.month:
                        if day.isoweekday() == 5:
                            days += 1
                        day += single_day
                    today = date_from
                    day=date(int(now.year), int(month) ,1)
                    single_day = timedelta(days=1)
                    weekday = month
                    dayss = 0
                    while day.month == today.month:
                        if day.isoweekday() == 7:
                            dayss += 1
                        day += single_day
                    week_day = dayss + days
                    monthday =  date_to - date_from 
                    monthday += timedelta(days=1)
                    total_day = (monthday.days) - week_day
                    total_hour = total_day * employee.resource_calendar_id.hours_per_day
                    employee.total_day = total_day
                    employee.total_hour = total_hour
                    employee.present_day = total_day       
        return {       
            'employee_ids':employee_ids,
            'docs': docs,
            'date_from':start_date,
            'date_to':end_date,
            'manager':manager,     
    }
