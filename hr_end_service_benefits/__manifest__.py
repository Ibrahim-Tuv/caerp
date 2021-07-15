# -*- coding: utf-8 -*-
{
    'name': """Employee End Of Service Rewards""",
    'summary': """End Of Service reward for years of services, approvals and disbursements""",
    'description': """Create and Calculate your employees END OF SERVICE Reward""",
    'author': 'I VALUE Solutions',
    'website': 'https://ivalue-s.com',
    'email': 'info@ivalue-s.com',
    'license': 'OPL-1',
    'price': 129.99,
    'currency': 'EUR',
    'images': ['static/description/Banner.png'],
    'version': '0.2',
    'depends': ['portal', 'web', 'hr_contract_allowances', 'account','hr_payroll'],
    'category': 'HR',
    'data': [
        'data/data.xml',
        'data/types_data.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizards/settlement_views.xml',
        'views/hr_end_service_benefit_views.xml',
        'views/hr_end_service_benefit_type_views.xml',
        'views/hr_employee_views.xml',
        'views/config_views.xml',
        'reports/ending_service_report.xml',
        # 'reports/ending_service_reports/_wizard.xml',
        # 'reports/report_ending_service.xml',

    ],
    'demo': []
}
