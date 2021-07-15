# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Ascetic Business Solution <www.asceticbs.com>
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
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta
import time 
import base64 
import calendar 
from odoo.tests.common import Form

class Employee(models.Model):
    _inherit = "hr.employee"

    total_day = fields.Char('day')
    total_hour = fields.Char('hour')
    present_day = fields.Char('present day')
    date_from = fields.Date('Date from')
    date_to = fields.Date('Date to')

    #send mail functionality
    def send_employee_report(self):
        employee_ids = self.env['hr.employee'].search([])
        manager_ids = []
        for employee in employee_ids:
            if employee.parent_id and employee.parent_id  not in manager_ids :
                manager_ids.append(employee.parent_id)
                for manager in manager_ids :
                    for res_user_id in self.env['res.users'].search([]):
                        partner_list = []
                        email_to =[]
                        report_mail = {}
                        now = datetime.now()
                        year = now.year
                        month = now.month
                        month_date=date(int(now.year),int(now.month),1)
                        date_from=month_date.replace(day=1)
                        today_date = date.today()
                        if today_date == date_from :
                            if res_user_id.has_group('hr.group_hr_manager'):
                                partner_list.append(res_user_id.partner_id.id)
                                content = "Please Find Attachment"
                                report_mail = {
                                    'subject'   : "Employee Attandance Report",
                                    'email_to': manager.name ,
                                    'author_id' :  res_user_id.partner_id.id,
                                    'body_html' :  content,
                                       }
                                name = "my attachment"
                                pdf = self.env.ref('abs_monthly_attendance_report.single_manager').render_qweb_pdf(manager.id)
                                b64_pdf = base64.b64encode(pdf[0])
                                attachment = self.env['ir.attachment'].create ({
                                    'name'   : 'Attendance report for the '  + manager.name,
                                    'type' : 'binary',
                                    'datas':  b64_pdf,
                                    'res_model' :  self._name,
                                    'res_id' :  self.id,
                                    'mimetype' :  'application/x-pdf'
                                       })
                           
                                if report_mail:
                                    mail_id = res_user_id.env['mail.mail'].sudo().create(report_mail)
                                    if mail_id:
                                        mail_id.send(res_user_id.id)
                                        mail_id.attachment_ids=[(6,0,[attachment.id])]

