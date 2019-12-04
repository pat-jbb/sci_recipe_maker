# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Recipe Maker',
    'version': '12.0',
    'summary': 'Generate Recipe and show to blogs',
    'author': 'SCI GLOBAL SERVICES',
    'description': """ 
        """,
    'depends': [
        'base', 'web'
    ],
    'data': [
        'security/recipe_security.xml',
        'security/ir.model.access.csv',
        'views/recipe_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
