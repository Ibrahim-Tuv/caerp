# -- coding: utf-8 --
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.


import logging

from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from odoo.addons.resource.models.resource import HOURS_PER_DAY

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class HolidaysAllocation(models.Model):
    _inherit = 'hr.leave.allocation'

    allocation_at = fields.Selection([
        ('employee_create_date', 'Based on Employee Creation Date'),
        ('month_beginning', 'Beginning of the Month'),
        ('month_ending', 'End of the Month'),
        ('joining_date', 'Based on Joining date'),
    ], default='employee_create_date', string='Allocation at')

    @api.model
    def _update_accrual(self):
        """
            Method called by the cron task in order to increment the number_of_days when
            necessary.
        """
        today = fields.Date.from_string(fields.Date.today())

        holidays = self.search(
            [('allocation_type', '=', 'accrual'), ('employee_id.active', '=', True), ('state', '=', 'validate'),
             ('holiday_type', '=', 'employee'),
             '|', ('date_to', '=', False), ('date_to', '>', fields.Datetime.now()),
             '|', ('nextcall', '=', False), ('nextcall', '<=', today)])

        for holiday in holidays:
            values = {}

            delta = relativedelta(days=0)

            if holiday.interval_unit == 'weeks':
                delta = relativedelta(weeks=holiday.interval_number)
            if holiday.interval_unit == 'months':
                delta = relativedelta(months=holiday.interval_number)
            if holiday.interval_unit == 'years':
                delta = relativedelta(years=holiday.interval_number)

            values['nextcall'] = (holiday.nextcall if holiday.nextcall else today) + delta

            period_start = datetime.combine(today, time(0, 0, 0)) - delta
            period_end = datetime.combine(today, time(0, 0, 0))

            # We have to check when the employee has been created
            # in order to not allocate him/her too much leaves
            start_date = holiday.employee_id._get_date_start_work()
            if holiday.allocation_at == 'employee_create_date':
                return super(HolidaysAllocation, self)._update_accrual()
            elif holiday.allocation_at == 'month_beginning':
                start_date = fields.Date.today().replace(day=1)
            elif holiday.allocation_at == 'month_ending':
                start_date = (fields.Date.today() + relativedelta(months=1)) - relativedelta(days=1)
            elif holiday.allocation_at == 'joining_date':
                start_date = holiday.employee_id.joining_date
            start_date = datetime.combine(start_date, time(0, 0, 0))
            # If employee is created after the period, we cancel the computation
            if period_end <= start_date:
                holiday.write(values)
                continue

            # If employee created during the period, taking the date at which he has been created
            if period_start <= start_date:
                period_start = start_date

            worked = holiday.employee_id._get_work_days_data(period_start, period_end,
                                                             domain=[('holiday_id.holiday_status_id.unpaid', '=', True),
                                                                     ('time_type', '=', 'leave')])['days']
            left = holiday.employee_id._get_leave_days_data(period_start, period_end,
                                                            domain=[('holiday_id.holiday_status_id.unpaid', '=', True),
                                                                    ('time_type', '=', 'leave')])['days']
            prorata = worked / (left + worked) if worked else 0

            days_to_give = holiday.number_per_interval
            if holiday.unit_per_interval == 'hours':
                # As we encode everything in days in the database we need to convert
                # the number of hours into days for this we use the
                # mean number of hours set on the employee's calendar
                days_to_give = days_to_give / (holiday.employee_id.resource_calendar_id.hours_per_day or HOURS_PER_DAY)

            values['number_of_days'] = holiday.number_of_days + days_to_give * prorata
            if holiday.accrual_limit > 0:
                values['number_of_days'] = min(values['number_of_days'], holiday.accrual_limit)

            holiday.write(values)
