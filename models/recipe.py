# -*- coding: utf-8 -*-
from collections import OrderedDict
from odoo.tools import html2plaintext
from odoo.http import request
from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug


class RecipeRecipe(models.Model):
    _inherit = "blog.post"
    _description = "Recipe Maker"

    is_recipe = fields.Boolean("Is a Recipe")
    is_featured_gourmet = fields.Boolean("Is Featured Gourmet")
    # recipe_name = fields.Char("Recipe Name")
    # TODO: Remove summary and transfer to tge default subtitle field
    summary = fields.Text("Summary")
    author = fields.Char("Author")
    about_author = fields.Text("About the Author")
    servings = fields.Char("Servings")
    servings_type = fields.Char("Servings Type", default="People")
    calories = fields.Integer("Calories")
    # TODO: Create a method that gets the ISO 8601 time duration format
    # TODO: Create a method that converts mins to hour-minute
    prep_time = fields.Integer("Prep Time")
    cook_time = fields.Integer("Cook Time")
    total_time = fields.Integer("Total Time")
    course_ids = fields.Many2many('recipe.course', string='Course')
    cuisine_ids = fields.Many2many('recipe.cuisine', string='Cuisine')

    ingredient_line_ids = fields.One2many('ingredient.line', 'recipe_id', string='Ingredients')
    instruction_line_ids = fields.One2many('instruction.line', 'recipe_id', string='Instructions')

    notes = fields.Html("Recipe Notes", translate=True)
    image_caption = fields.Char("Recipe Image Caption")
    image = fields.Binary("Image", attachment=True,
                          help="This field holds the image used as avatar for this recipe, limited to 1024x1024px", )
    image_medium = fields.Binary("Medium-sized image", attachment=True,
                                 help="Medium-sized image of this contact. It is automatically " \
                                      "resized as a 128x128px image, with aspect ratio preserved. " \
                                      "Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized image", attachment=True,
                                help="Small-sized image of this contact. It is automatically " \
                                     "resized as a 64x64px image, with aspect ratio preserved. " \
                                     "Use this field anywhere a small image is required.")

    @api.model
    def _get_published_date(self):
        return

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
        if bool(self.notes) and self.notes == "<p><br></p>":
            return False
        return True

    def _get_structured_data(self):
        self.ensure_one()
        base_url = self.website_id and self.website_id.domain.rstrip('/')
        post_url = '%s/blog/%s/post/%s/#wrap' % (base_url, slug(self.blog_id), slug(self))
        author_name = self.sudo().author_id.name

        data = {"@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "WebSite",
                        "@id": "%s/#wrap" % base_url,
                        "url": "%s" % base_url,
                        "name": "Qualifirst Blog",
                        "potentialAction": {
                            "@type": "SearchAction",
                            "target": "%s/search?q={search_term_string}" % base_url,
                            "query-input": "required q=search_term_string"
                        }
                    },
                    {
                        "@type": "WebPage",
                        "@id": "%s/#wrap" % base_url,
                        "url": "%s" % base_url,
                        "inLanguage": "en-US",
                        # TODO: Add meta fields
                        "name": "Vegan White Beans with Smoked Nuckhen Recipe - THE new vegan meat.",
                        "isPartOf": {
                            "@id": "%s/#website" % base_url
                        },
                        "primaryImageOfPage": {
                            "@id": "%s/#primaryimage" % base_url
                        },
                        # TODO: Add a method to get the published date using the format below
                        "datePublished": "2018-04-24T18:39:47+00:00",
                        "dateModified": "2019-01-11T19:35:56+00:00",
                        "author": {
                            # TODO: Check person schema in the old blog site
                            "@id": "%s/#/schema/person/d89e1f0edb9e60a39900bb2afadafa00" % base_url
                        },
                        "description": "%s" % self.subtitle
                    },
                    {
                        "@type": [
                            "Person"
                        ],
                        # TODO: Check ID
                        "@id": "%s/#/schema/person/d89e1f0edb9e60a39900bb2afadafa00" % base_url,
                        "name": "%s" % author_name,
                        "image": {
                            "@type": "ImageObject",
                            "@id": "%s/#authorlogo" % base_url,
                            "url": "%s" % self.sudo().author_id.gravatar_image_url,
                            "caption": "%s" % author_name
                        },
                        # TODO: Inherit res partner and add about author description
                        "description": "%s" % self.sudo().author_id.about_author,
                        "sameAs": [
                            # TODO: Check for author's social urls
                            "https://www.linkedin.com/in/jodi-mackinnon-9511b620/"
                        ]
                    },
                    {
                        "@context": "http://schema.org/",
                        "@type": "Recipe",
                        "name": "%s" % self.name,
                        "author": {
                            "@type": "Person",
                            "name": "%s" % self.author or author_name
                        },
                        "description": "%s" % self.subtitle,
                        # TODO: Add a method that formats the publishing date-->
                        "datePublished": "2018-04-24T13:39:47+00:00",
                        # TODO: Get all images?
                        "image": [
                            "https://blog.qualifirst.com/wp-content/uploads/2018/04/Nuckhen-Beans.jpg",
                            "https://blog.qualifirst.com/wp-content/uploads/2018/04/Nuckhen-Beans-500x500.jpg",
                            "https://blog.qualifirst.com/wp-content/uploads/2018/04/Nuckhen-Beans-500x375.jpg",
                            "https://blog.qualifirst.com/wp-content/uploads/2018/04/Nuckhen-Beans-480x270.jpg"
                        ],
                        # TODO: Add a method that adds converts minutes to hour-minute format
                        "prepTime": "PT%sM" % self.prep_time,
                        "cookTime": "PT%sM" % self.cook_time,
                        "totalTime": "PT%sM" % self.total_time,
                        # TODO: Check if in order
                        "recipeIngredient": [
                            "%s%s%s%s" % (
                                ing.amount or '', ing.unit and ' %s' % ing.unit or '',
                                ing.name and ' %s' % ing.name or '',
                                ing.note and ', %s' % ing.note or '') for ing in self.ingredient_line_ids
                        ],
                        "recipeInstructions": [{
                            "@type": "HowToStep",
                            "text": "%s" % ins.name
                        } for ins in self.instruction_line_ids
                        ],
                        # TODO: Check other categories (Course??)
                        "recipeCategory": [course.name for course in self.course_ids],
                        "recipeCuisine": [cuisine.name for cuisine in self.cuisine_ids],
                        "@id": "%s/#recipe" % post_url,
                        "isPartOf": {
                            "@id": "%s/#wrap" % post_url
                        },
                        "mainEntityOfPage": "%s/#wrap" % post_url
                    }]
                }

        if self.image_medium:
            data['@graph'].append({
                "@type": "ImageObject",
                "@id": "%s/#primaryimage" % post_url,
                "url": "%s/web/image/blog.post/%s/image_medium" % (base_url, self.id),
                # "width": 3170,
                # "height": 1642,
                # TODO: Add main image caption field
                "caption": "%s" % self.image_caption or '%s Image' % self.name
            })

        return


class RecipeTag(models.Model):
    _inherit = "blog.tag"

    website_id = fields.Many2one('website', string='Website', help='Restrict publishing to this website.')

    @api.multi
    def can_access_from_current_website(self, website_id=False):
        can_access = True
        for record in self:
            if (website_id or record.website_id.id) not in (False, request.website.id):
                can_access = False
                continue
        return can_access


class RecipeCourse(models.Model):
    _name = 'recipe.course'
    _description = 'Course Recipe'
    _inherit = "website.multi.mixin"
    _order = 'name'

    name = fields.Char('Name', required=True, translate=True)
    blog_ids = fields.Many2many('blog.post', string='Recipes')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Course already exists !"),
    ]


class RecipeCuisine(models.Model):
    _name = 'recipe.cuisine'
    _description = 'Cuisine Recipe'
    _inherit = "website.multi.mixin"
    _order = 'name'

    name = fields.Char('Name', required=True, translate=True)
    blog_ids = fields.Many2many('blog.post', string='Recipes')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Cuisine already exists !"),
    ]
