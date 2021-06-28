# -*- coding: utf-8 -*-
# Copyright 2018 Openinside co. W.L.L.
{
    "name": "Show Duration in Leave Allocation",
    "summary": "Show Duration in Leave Allocation",
    "version": "13.0.1.1.0",
    'category': 'Human Resources',
    "website": "https://www.open-inside.com",
	"description": """
		* Show Duration in Leave Allocation
		* get_leave_balance method in hr.employee to get balance for specific date to use it in payroll rules
    """,
	'images':[
        
	],
    "author": "Openinside",
    "license": "OPL-1",
    "price" : 0,
    "currency": 'EUR',
    "installable": True,
    "depends": [
        'hr_holidays'
    ],
    "data": [
        'view/hr_leave_allocation.xml'
    ],
    'odoo-apps' : True    
}

