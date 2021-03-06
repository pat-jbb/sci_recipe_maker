# -*- coding: utf-8 -*-
from collections import OrderedDict
import json
from odoo.http import request
from odoo.tools import html2plaintext
from odoo import api, fields, models
from odoo.addons.http_routing.models.ir_http import slug

ISO8601_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


class RecipeRecipe(models.Model):
    _name = 'blog.post'
    _inherit = ['blog.post', 'image.mixin']

    is_recipe = fields.Boolean("Is a Recipe")
    is_featured_gourmet = fields.Boolean("Featured Gourmet")
    summary = fields.Text("Summary")
    author = fields.Char("Author Name")
    about_author = fields.Text("About the Author")
    servings = fields.Char("Servings")
    servings_type = fields.Char("Servings Type", default="People")
    calories = fields.Integer("Calories")
    prep_time = fields.Integer("Prep Time")
    cook_time = fields.Integer("Cook Time")
    total_time = fields.Integer("Total Time")
    course_ids = fields.Many2many('recipe.course', string='Course')
    cuisine_ids = fields.Many2many('recipe.cuisine', string='Cuisine')

    ingredient_line_ids = fields.One2many('ingredient.line', 'recipe_id', string='Ingredients')
    instruction_line_ids = fields.One2many('instruction.line', 'recipe_id', string='Instructions')

    notes = fields.Html("Recipe Notes", translate=True)
    image_caption = fields.Char("Image Caption")

    @api.model
    def _get_hm_format(self, t_min):
        if t_min == 60:
            ptm = "1 hr"
        elif t_min > 60:
            t_hr = t_min // 60
            rem_min = t_min % 60
            rem_min_txt = rem_min and ' %s mins' % rem_min or ''
            ptm = "%s hrs%s" % (t_hr, rem_min_txt)
        else:
            ptm = "%s mins" % t_min
        return ptm

    @api.model
    def get_recipe_groups(self, obj):
        group = OrderedDict()
        group_name = None
        for line in obj:
            if line.is_group:
                group_name = line.name
                continue
            if group_name:
                if not group.get(group_name):
                    group[group_name] = []
                group[group_name].append(line)
            else:
                if not group.get('no_group'):
                    group['no_group'] = []
                group['no_group'].append(line)
        return group

    @api.model
    def has_notes(self):
        return html2plaintext(self.notes) and True or False

    def get_structured_data(self):
        # TODO: Add rating, nutrition, video schema, use py library instead?
        self.ensure_one()
        current_website = self.env['website'].get_current_website()
        base_url = current_website and current_website.domain.rstrip('/')
        # TODO: Update to get the SEOd Blog URL
        post_url = '%s/blog/%s/post/%s' % (base_url, slug(self.blog_id), slug(self))
        author_id = self.sudo().author_id
        author_name = author_id.name
        pub_date = self.published_date
        wr_date = self.write_date

        published_date = pub_date and pub_date.strftime(ISO8601_FORMAT) or ""
        write_date = wr_date and wr_date.strftime(ISO8601_FORMAT) or ""

        schema_data = OrderedDict()
        schema_data["@context"] = "https://schema.org"
        schema_data["@graph"] = []
        schema_data["@graph"].append({
            "@type": "WebSite",
            "@id": "%s/#wrap" % base_url,
            "url": "%s" % base_url,
            "name": "Qualifirst Blog",
            "potentialAction": {
                "@type": "SearchAction",
                "target": "%s/search?q={search_term_string}" % base_url,
                "query-input": "required q=search_term_string"
            }
        })
        schema_data["@graph"].append({
            "@type": "WebPage",
            "@id": "%s/#wrap" % base_url,
            "url": "%s" % base_url,
            # TODO: dynamic inLanguage ?
            "inLanguage": "en-US",
            "name": "%s" % self.website_meta_title,
            "isPartOf": {
                "@id": "%s/#website" % base_url
            },
            "primaryImageOfPage": {
                "@id": "%s/#primaryimage" % base_url
            },
            "datePublished": "%s" % published_date,
            "dateModified": "%s" % write_date,
            "description": "%s" % self.website_meta_description
        })

        if author_id.gravatar_image_url and author_id.about_author:
            schema_data["@graph"].append({
                "@type": "Person",
                "name": "%s" % author_name,
                "image": {
                    "@type": "ImageObject",
                    "@id": "%s/#authorlogo" % base_url,
                    "url": "%s" % author_id.gravatar_image_url or '',
                    "caption": "%s" % author_name
                },
                "description": "%s" % html2plaintext(author_id.about_author),
                "sameAs": author_id.get_partner_social()
            })

        if self.is_recipe and self.ingredient_line_ids:
            schema_data["@graph"].append({
                "@context": "http://schema.org/",
                "@type": "Recipe",
                "name": "%s" % self.name,
                "author": {
                    "@type": "Person",
                    "name": "%s" % (self.author or author_name)
                },
                "description": "%s" % self.subtitle,
                "datePublished": "%s" % published_date,
                # TODO: Implement multiple images here, change URL
                "image": ["%s/web/image/blog.post/%s/image_medium" % (base_url, self.id)],
                "prepTime": "PT%sM" % self.prep_time,
                "cookTime": "PT%sM" % self.cook_time,
                "totalTime": "PT%sM" % self.total_time,
                "recipeIngredient": [
                    "%s%s%s%s" % (
                        ing.amount or '', ing.unit and ' %s' % ing.unit or '',
                        ing.name and ' %s' % ing.name or '',
                        ing.notes and ', %s' % ing.notes or '') for ing in self.ingredient_line_ids
                ],
                "recipeInstructions": [{
                    "@type": "HowToStep",
                    "text": "%s" % ins.name
                } for ins in self.instruction_line_ids
                ],
                "recipeCategory": [course.name for course in self.course_ids],
                "recipeCuisine": [cuisine.name for cuisine in self.cuisine_ids],
                "@id": "%s/#recipe" % post_url,
                "isPartOf": {
                    "@id": "%s/#wrap" % post_url
                },
                "mainEntityOfPage": "%s/#wrap" % post_url})

            if self.image_medium:
                schema_data["@graph"].append({
                    "@type": "ImageObject",
                    "@id": "%s/#primaryimage" % post_url,
                    "url": "%s/web/image/blog.post/%s/image_medium" % (base_url, self.id),
                    "caption": "%s" % self.image_caption or '%s Image' % self.name
                })

        return json.dumps(schema_data)


class RecipeTag(models.Model):
    _inherit = "blog.tag"

    subtitle = fields.Char('Sub Title', translate=True)
    website_id = fields.Many2one('website', string='Website', help='Restrict publishing to this website.')
    website_ids = fields.Many2many('website', string='Websites')

    def can_access_from_current_website(self, website_id=False):
        can_access = True
        for record in self:
            if (website_id or record.website_id.id or record.website_id.ids) not in (False, request.website.id):
                can_access = False
                continue
        return can_access


class RecipeCourse(models.Model):
    _name = 'recipe.course'
    _description = 'Course Recipe'
    _inherit = ['website.multi.mixin', 'mail.thread']
    _order = 'name'

    name = fields.Char('Name', required=True, translate=True)
    blog_ids = fields.Many2many('blog.post', string='Recipes')
    subtitle = fields.Char('Sub Title', translate=True)
    website_ids = fields.Many2many('website', string='Websites')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Course already exists !"),
    ]

    def can_access_from_current_website(self, website_id=False):
        can_access = True
        for record in self:
            if (website_id or record.website_id.id) not in (False, request.website.id) or request.website.id in record.website_ids.ids:
                can_access = False
                continue
        return can_access


class RecipeCuisine(models.Model):
    _name = 'recipe.cuisine'
    _description = 'Cuisine Recipe'
    _inherit = ['website.multi.mixin', 'mail.thread']
    _order = 'name'

    name = fields.Char('Name', required=True, translate=True)
    blog_ids = fields.Many2many('blog.post', string='Recipes')
    subtitle = fields.Char('Sub Title', translate=True)
    website_ids = fields.Many2many('website', string='Websites')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Cuisine already exists !"),
    ]

    def can_access_from_current_website(self, website_id=False):
        can_access = True
        for record in self:

            if (website_id or record.website_id.id or record.website_id.ids) not in (False, request.website.id):
                can_access = False
                continue
        return can_access
