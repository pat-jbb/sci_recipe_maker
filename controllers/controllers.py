# -*- coding: utf-8 -*-
from odoo import http
import werkzeug
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import unslug
from odoo.addons.website_blog.controllers.main import WebsiteBlog
from odoo.addons.website.controllers.main import QueryURL


class WebsiteBlog(WebsiteBlog):

    @http.route([
        '/tag/<model("blog.tag"):tag>',
        '/tag/<model("blog.tag"):tag>/page/<int:page>'], type='http', auth="public", website=True)
    def recipe_tags(self, tag=None, page=1, **post):

        if not tag:
            return werkzeug.utils.redirect('/blog')

        if not tag.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        return request.render("sci_recipe_maker.recipe_tag_template", {
            'blog': tag,
            'blog_posts': tag.post_ids,
        })

    @http.route([
        '/course/<model("recipe.course"):course>',
        '/course/<model("recipe.course"):course>/page/<int:page>'], type='http', auth="public", website=True)
    def recipe_courses(self, course=None, page=1, **post):

        if not course:
            return werkzeug.utils.redirect('/blog')

        if not course.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        return request.render("sci_recipe_maker.recipe_tag_template", {
            'blog': course,
            'blog_posts': course.blog_ids,
        })
