# -- coding: utf-8 --
# This module and its content is copyright of Technaureus Info Solutions Pvt. Ltd.
# - © Technaureus Info Solutions Pvt. Ltd 2020. All rights reserved.

{
    'name': 'Accrual Advanced',
    'version': '13.0.0.1',
    'category': 'Human Resources',
    'sequence': 1,
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'summary': 'Advanced Accrual Leaves Allocation.',
    'description': """Advanced Accrual Leaves Allocation""",
    'website': 'http://www.technaureus.com',
    'depends': ['hr_holidays'],
    'price': 19.99,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'data': [
        'views/hr_leave_allocation_views.xml',
        'views/hr_employee_views.xml',
    ],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False
}
