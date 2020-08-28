# -*- coding: utf-8 -*-
{
    'name': 'Recipe Maker',
    'category': 'Website/Website',
    'sequence': 200,
    'version': '13.0',
    'summary': 'Generate and Publish Recipes',
    'author': 'SCI GLOBAL SERVICES INC.',
    'description': "",
    'depends': ['website_blog'],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/recipe_views.xml',
        'views/partner_views.xml',
        'views/recipe_template.xml',
        'views/recipe_assets.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
