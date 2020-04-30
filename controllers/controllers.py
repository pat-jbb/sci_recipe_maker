# -*- coding: utf-8 -*-
from odoo import http
import werkzeug
import json
from odoo.http import request
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
        blog_posts = tag.post_ids
        pager = request.website.pager(
            url=request.httprequest.path.partition('/page/')[0],
            total=len(blog_posts),
            page=page,
            step=self._blog_post_per_page,
        )
        pager_begin = (page - 1) * self._blog_post_per_page
        pager_end = page * self._blog_post_per_page
        blog_posts = blog_posts[pager_begin:pager_end]

        return request.render("website_blog.blog_post_short", {
            'blog': tag,
            'blog_url': QueryURL(),
            'state_info': {"state": '', "published": '', "unpublished": ''},
            'main_object': tag,
            'blog_posts': blog_posts,
            'pager': pager,
            'active_tag_ids': [],
            'blog_posts_cover_properties': [json.loads(b.cover_properties) for b in blog_posts],
            'tag_category': [],
        })

    @http.route([
        '/course/<model("recipe.course"):course>',
        '/course/<model("recipe.course"):course>/page/<int:page>'], type='http', auth="public", website=True)
    def recipe_courses(self, course=None, page=1, **post):

        if not course:
            return werkzeug.utils.redirect('/blog')

        if not course.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        blog_posts = course.blog_ids
        pager = request.website.pager(
            url=request.httprequest.path.partition('/page/')[0],
            total=len(blog_posts),
            page=page,
            step=self._blog_post_per_page,
        )
        pager_begin = (page - 1) * self._blog_post_per_page
        pager_end = page * self._blog_post_per_page
        blog_posts = blog_posts[pager_begin:pager_end]

        return request.render("website_blog.blog_post_short", {
            'blog': course,
            'blog_url': QueryURL(),
            'state_info': {"state": '', "published": '', "unpublished": ''},
            'main_object': course,
            'blog_posts': blog_posts,
            'pager': pager,
            'active_tag_ids': [],
            'blog_posts_cover_properties': [json.loads(b.cover_properties) for b in blog_posts],
            'tag_category': [],
        })
