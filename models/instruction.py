from odoo import api, fields, models, _


class RecipeInstruction(models.Model):
    _name = "instruction.line"
    _description = "Recipe Instruction"
    _order = "sequence, id"

    name = fields.Text('Instruction', required=True)
    sequence = fields.Integer('Sequence')
    is_group = fields.Boolean('Group')
    recipe_id = fields.Many2one('blog.post', ondelete='cascade', string='Recipe')
    image = fields.Binary("Image", attachment=True,
                          help="This field holds the image used as avatar for this recipe instruction, "
                               "limited to 1024x1024px", )
    image_medium = fields.Binary("Medium-sized image", attachment=True,
                                 help="Medium-sized image of this contact. It is automatically " \
                                      "resized as a 128x128px image, with aspect ratio preserved. " \
                                      "Use this field in form views or some kanban views.")
