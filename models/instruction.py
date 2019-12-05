from odoo import api, fields, models, _


class RecipeInstruction(models.Model):
    _name = "instruction.line"
    _description = "Recipe Instruction"
    _order = "sequence, id"

    name = fields.Text('Instruction', required=True)
    sequence = fields.Integer('Sequence')
    is_group = fields.Boolean('Instruction Group')
    recipe_id = fields.Many2one('blog.post', ondelete='cascade', string='Recipe')
