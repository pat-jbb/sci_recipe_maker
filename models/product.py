from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def get_related_recipes(self, limit=None):
        recipes = self.env['blog.post'].search([('ingredient_line_ids.product_id', 'in', self.product_variant_ids.ids),
                                                ('website_published', '=', True)], limit=limit)
        return recipes
