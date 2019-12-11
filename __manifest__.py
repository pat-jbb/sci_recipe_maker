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
        'base', 'web', 'website_blog'
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/recipe_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
