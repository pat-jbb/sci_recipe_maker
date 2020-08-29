from odoo import api, fields, models
from odoo.tools import html2plaintext

class ResPartner(models.Model):
    _inherit = "res.partner"

    about_author = fields.Html("About Author", help="The About the Author description in the blog post")
    gravatar_image_url = fields.Char("Gravatar Image URL", help="Gravatar URL of the Blog Author")
    social_twitter = fields.Char('Twitter Account')
    social_facebook = fields.Char('Facebook Account')
    social_github = fields.Char('GitHub Account')
    social_linkedin = fields.Char('LinkedIn Account')
    social_youtube = fields.Char('Youtube Account')
    social_googleplus = fields.Char('Google+ Account')
    social_instagram = fields.Char('Instagram Account')

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

    @api.model
    def has_about_author(self):
        return html2plaintext(self.about_author) and True or False