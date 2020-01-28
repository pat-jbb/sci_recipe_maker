from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.one
    def get_related_recipes(self):
        recipe_ingredient_model = self.env['ingredient.line']
        recipe_ids = recipe_ingredient_model.search([('product_id', 'in', self.product_variant_ids.ids)]).mapped(
            'recipe_id')
        if recipe_ids:
            recipe_ids = [recipe[0] for recipe in recipe_ids]
        return recipe_ids
