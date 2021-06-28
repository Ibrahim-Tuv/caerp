# -*- coding: utf-8 -*-
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class AutomaticLeaveAllocation(models.Model):
    _name = "automatic.leave.allocation"
    _description = "Automatic Leave Allocation"
    _inherit = ['mail.thread']

    name = fields.Char('Description')
    active = fields.Boolean('Active', default=True)
    leave_type_id = fields.Many2one("hr.leave.type",
                                    string="Leave Type", copy=False,
                                    track_visibility='onchange')
    type_request_unit = fields.Selection(
        related='leave_type_id.request_unit', readonly=True)
    type = fields.Selection(
        [('prorata', 'Pro-Rata'), ('full', 'Full')], string='Type',
        track_visibility='onchange', copy=False, default='full')
    no_of_days = fields.Float('No of Days', track_visibility='onchange')
    no_of_hours = fields.Float('No of Hours', track_visibility='onchange')
    last_alloc_date = fields.Date('Last Allocation Date',
                                  track_visibility='onchange')
    next_alloc_date = fields.Date('Next Allocation Date')
    alloc_by = fields.Selection([('by_emp', 'By Employee'),
                                 ('by_company', 'By Company'),
                                 ('by_dept', 'By Department'),
                                 ('by_tag', 'By Employee Tag')],
                                default='by_emp',
                                string='Allocation By',
                                track_visibility='onchange')
    emp_ids = fields.Many2many('hr.employee',
                               string='Employees',
                               track_visibility='onchange')
    company_id = fields.Many2one(
        'res.company',
        default=lambda self: self.env.user.company_id.id,
        track_visibility='onchange')
    dept_ids = fields.Many2many('hr.department',
                                string='Departments',
                                track_visibility='onchange')
    tag_ids = fields.Many2many('hr.employee.category',
                               string='Tags',
                               track_visibility='onchange')

    def alloc_leaves(self):
        """
        This method is used to allocate leaves based on the configuration.
        ------------------------------------------------------------------
        @param self: object pointer
        """
        alloc_obj = self.env['hr.leave.allocation']
        for al in self:
            if not al.next_alloc_date:
                al.next_alloc_date = fields.Date.today()
            if al.next_alloc_date <= fields.Date.today():
                if al.alloc_by == 'by_emp':
                    # Create Allocations for Employee
                    for emp in al.emp_ids:
                        vals = {
                            'name': 'Auto-Leave Allocation for ' + emp.name,
                            'holiday_status_id': al.leave_type_id.id,
                            'holiday_type': 'employee',
                            'employee_id': emp.id,
                        }
                        if al.type_request_unit == 'hour':
                            vals.update({'number_of_days': al.no_of_hours})
                        else:
                            vals.update({'number_of_days': al.no_of_days})
                        alloc = alloc_obj.create(vals)
                        # Approve Allocations for Employee
                        alloc.action_approve()
                        # Validate Allocations for Employee
                        if al.leave_type_id.validation_type == 'both':
                            alloc.action_validate()
                elif al.alloc_by == 'by_company':
                    # Create Allocations for Company
                    vals = {
                        'name': 'Auto-Leave Allocation for \
                        ' + al.company_id.name,
                        'holiday_status_id': al.leave_type_id.id,
                        'holiday_type': 'company',
                        'mode_company_id': al.company_id.id,
                        'employee_id': False,
                    }
                    print ("=vals",vals)
                    if al.type_request_unit == 'hour':
                        vals.update({'number_of_days': al.no_of_hours})
                    else:
                        vals.update({'number_of_days': al.no_of_days})
                    alloc = alloc_obj.create(vals)
                    # Approve Allocations for Company
                    alloc.action_approve()
                    # Validate Allocations for Company
                    if al.leave_type_id.validation_type == 'both':
                        alloc.action_validate()
                elif al.alloc_by == 'by_dept':
                    for dept in al.dept_ids:
                        # Create Allocations for Department
                        vals = {
                            'name': 'Auto-Leave Allocation for ' + dept.name,
                            'holiday_status_id': al.leave_type_id.id,
                            'holiday_type': 'department',
                            'department_id': dept.id,
                            'employee_id': False,
                        }
                        if al.type_request_unit == 'hour':
                            vals.update({'number_of_days': al.no_of_hours})
                        else:
                            vals.update({'number_of_days': al.no_of_days})
                        alloc = alloc_obj.create(vals)
                        # Approve Allocations for Department
                        alloc.action_approve()
                        # Validate Allocations for Department
                        if al.leave_type_id.validation_type == 'both':
                            alloc.action_validate()
                elif al.alloc_by == 'by_tag':
                    for tag in al.tag_ids:
                        # Create Allocations for Employee Tag
                        vals = {
                            'name': 'Auto-Leave Allocation for ' + tag.name,
                            'holiday_status_id': al.leave_type_id.id,
                            'holiday_type': 'category',
                            'category_id': tag.id,
                            'employee_id': False,
                        }
                        if al.type_request_unit == 'hour':
                            vals.update({'number_of_days': al.no_of_hours})
                        else:
                            vals.update({'number_of_days': al.no_of_days})
                        alloc = alloc_obj.create(vals)
                        # Approve Allocations for Employee Tag
                        alloc.action_approve()
                        # Validate Allocations for Employee Tag
                        if al.leave_type_id.validation_type == 'both':
                            alloc.action_validate()
                # Update the date as per the allocation type
                if al.type == 'prorata':
                    al.next_alloc_date = al.next_alloc_date + relativedelta(months=1)
                elif al.type == 'full':
                    al.next_alloc_date = al.next_alloc_date + relativedelta(years=1)
                al.last_alloc_date = fields.Date.today()

    @api.model
    def _auto_alloc_leaves(self):
        """
        This is a scheduler method that will check the dates and allocate the leaves
        ----------------------------------------------------------------------------
        @param self: object pointer
        """
        # Search for allocation configurations
        allocs = self.search(['|', ('next_alloc_date', '<=', fields.Date.today()),
                                   ('next_alloc_date', '=', False)])
        # Allocate Leaves
        allocs.alloc_leaves()
