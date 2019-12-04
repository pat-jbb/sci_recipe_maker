# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from odoo import api, fields, models, _


class RecipeRecipe(models.Model):
    _name = "recipe.recipe"
    _description = "Recipe"

    name = fields.Char("Name", required=True, translate=True)
    summary = fields.Text("Summary")
    author_id = fields.Many2one('res.partner', 'Author', default=lambda self: self.env.user.partner_id)
    servings = fields.Integer("Servings")
    calories = fields.Integer("Calories")
    prep_time = fields.Integer("Prep Time")
    cook_time = fields.Integer("Cook Time")
    total_time = fields.Integer("Total Time")
    course_ids = fields.Many2many('recipe.course', string='Course')
    cuisine_ids = fields.Many2many('recipe.cuisine', string='Course')
    active = fields.Boolean(string="Active", default=True)

    # ingredient_line = fields.One2many('ingredient.line', 'ingredient_id', string='Order Lines', states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True)

    # image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary("Image", attachment=True,
                          help="This field holds the image used as avatar for this contact, limited to 1024x1024px", )
    image_medium = fields.Binary("Medium-sized image", attachment=True,
                                 help="Medium-sized image of this contact. It is automatically " \
                                      "resized as a 128x128px image, with aspect ratio preserved. " \
                                      "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True,
                                help="Small-sized image of this contact. It is automatically " \
                                     "resized as a 64x64px image, with aspect ratio preserved. " \
                                     "Use this field anywhere a small image is required.")


class RecipeCourse(models.Model):
    _name = 'recipe.course'
    _description = 'Course Recipe'
    _order = 'name'

    name = fields.Char('Name', required=True, translate=True)
    recipe_ids = fields.Many2many('recipe.recipe', string='Recipes')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Recipe name already exists !"),
    ]


class RecipeCuisine(models.Model):
    _name = 'recipe.cuisine'
    _description = 'Cuisine Recipe'
    _order = 'name'

    name = fields.Char('Name', required=True, translate=True)
    recipe_ids = fields.Many2many('recipe.recipe', string='Recipes')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Recipe name already exists !"),
    ]
