# -*- coding: utf-8 -*-
{
    'name': "final_project",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'sequence': -500,
    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'contacts', 'om_account_accountant', 'accounting_pdf_reports'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/seq.xml',
        'views/menu.xml',
        'views/custom_tax.xml',
        'views/custom_accountant.xml',
        'views/custom_profitloss.xml',
        'views/custom_system.xml',



    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,

}
