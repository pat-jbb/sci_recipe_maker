from odoo import fields, models


class RecipeInstruction(models.Model):
    _name = "instruction.line"
    _inherit = ['image.mixin']
    _description = "Recipe Instruction"
    _order = "sequence, id"

    name = fields.Text('Instruction', required=True)
    sequence = fields.Integer('Sequence')
    is_group = fields.Boolean('Group')
    recipe_id = fields.Many2one('blog.post', ondelete='cascade', string='Recipe')