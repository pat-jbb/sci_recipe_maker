# -*- coding: utf-8 -*-
import werkzeug

from odoo import http
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request
from odoo.addons.website_blog.controllers.main import WebsiteBlog as WebsiteBlogController


class WebsiteBlog(WebsiteBlogController):

    @http.route([
        '''/course/<model("recipe.course"):course>''',
        '''/course/<model("recipe.course"):course>/page/<int:page>''',
    ], type='http', auth="public", website=True)
    def recipe_course(self, blog=None, course=None, tag=None, page=1, **opt):
        Blog = request.env['blog.blog']
        if not course:
            return werkzeug.utils.redirect('/blog')

        if course and not course.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        courses = course.blog_ids
        pager = request.website.pager(
            url=request.httprequest.path.partition('/page/')[0],
            total=len(courses),
            page=page,
            step=self._blog_post_per_page,
        )

        pager_begin = (page - 1) * self._blog_post_per_page
        pager_end = page * self._blog_post_per_page
        blog_posts = courses[pager_begin:pager_end]

        values = {
            'tag_category': [],
            'nav_list': self.nav_list(),
            'tags_list': self.tags_list,
            'pager': pager,
            'posts': blog_posts,
            'active_tag_ids': [],
            'blog': blog,
            'blogs': Blog,
            'blog_url': QueryURL(),
        }

        if course:
            values['main_object'] = course
            values['edit_in_backend'] = True

        return request.render("website_blog.blog_post_short", values)

