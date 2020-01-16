# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class BlogPost(models.Model):
    _inherit = "blog.post"
    _description = "Blog SEO"

    @api.constrains('website_meta_title', 'website_meta_description')
    def _check_meta_fields_length(self):
        for rec in self:
            err_message = ""
            if rec.website_meta_title:
                len_title = len(rec.website_meta_title)
                if len_title < 30 or len_title > 60:
                    err_message += "The recommended title length is between 30 to 60 characters\n" \
                                   "Current length: %s\n\n" % len_title
            if rec.website_meta_description:
                len_description = len(rec.website_meta_description)
                if len_description < 50 or len_description > 160:
                    err_message += "The recommended meta description length is between 50 to 160 characters.\n" \
                                   "Current length: %s" % len_description
            if err_message:
                raise ValidationError(err_message)
