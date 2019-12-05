from datetime import datetime, timedelta
from odoo import api, fields, models, _


class RecipeIngredients(models.Model):
    _name = "ingredient.line"
    _description = "Recipe Ingredients"
    _order = "sequence, id"

    name = fields.Text('Instruction', required=True)
    sequence = fields.Integer('Sequence')
    is_group = fields.Boolean('Instruction Group')
    recipe_id = fields.Many2one('blog.post', ondelete='cascade', string='Recipe')
