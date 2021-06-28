# -*- encoding: utf-8 -*-
##############################################################################
#
#    Skyscend Business Solutions
#    Copyright (C) 2019 (http://www.skyscendbs.com)
#
##############################################################################
{
    'name': 'Automatic Leave Allocation',
    'version': '13.0.0.1',
    'category': 'HR',
    'license': 'AGPL-3',
    'description': """
    Managing Employee's Leaves Automatically allocated.
    """,
    'author': 'Skyscend Business Solutions',
    'website': 'http://www.skyscendbs.com',
    'depends': ['hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'views/hr_holidays_view.xml',
    ],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False
}
