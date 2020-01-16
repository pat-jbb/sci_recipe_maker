# -*- coding: utf-8 -*-
{
    'name': 'Recipe Maker',
    'version': '12.0',
    'summary': 'Generate Recipe and show to blogs',
    'author': 'SCI GLOBAL SERVICES INC.',
    'description': """ 
        """,
    'depends': [
        'base', 'web', 'website_blog'
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/recipe_views.xml',
        'views/blog_seo_views.xml',
        'views/partner_views.xml',
        'views/recipe_template.xml',
        'views/recipe_assets.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
