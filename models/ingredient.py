from odoo import fields, models


class RecipeIngredients(models.Model):
    _name = 'ingredient.line'
    _description = "Recipe Ingredients"
    _order = "sequence, id"

    name = fields.Char("Name", required=True)
    sequence = fields.Integer("Sequence")
    amount = fields.Char("Amount")
    unit = fields.Char("Unit")
    notes = fields.Char("Notes")
    is_group = fields.Boolean("Group")
    product_id = fields.Many2one('product.product', string="Product")
    recipe_id = fields.Many2one('blog.post', ondelete='cascade', string="Recipe")
