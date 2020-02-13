from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    about_author = fields.Html("About Author", help="About the Author description in the blog post")
    gravatar_image_url = fields.Char("Gravatar Image URL", help="Blog post author Gravatar image url")
    social_twitter = fields.Char('Twitter Account')
    social_facebook = fields.Char('Facebook Account')
    social_github = fields.Char('GitHub Account')
    social_linkedin = fields.Char('LinkedIn Account')
    social_youtube = fields.Char('Youtube Account')
    social_googleplus = fields.Char('Google+ Account')
    social_instagram = fields.Char('Instagram Account')

    @api.multi
    def get_partner_social(self):
        self.ensure_one()
        socials = []
        if self.social_twitter:
            socials.append(self.social_twitter)
        if self.social_facebook:
            socials.append(self.social_facebook)
        if self.social_github:
            socials.append(self.social_github)
        if self.social_linkedin:
            socials.append(self.social_linkedin)
        if self.social_youtube:
            socials.append(self.social_youtube)
        if self.social_googleplus:
            socials.append(self.social_googleplus)
        if self.social_instagram:
            socials.append(self.social_instagram)
        return socials
