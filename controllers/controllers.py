# -*- coding: utf-8 -*-
# from odoo import http


# class Kursus(http.Controller):
#     @http.route('/kursus/kursus', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kursus/kursus/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kursus.listing', {
#             'root': '/kursus/kursus',
#             'objects': http.request.env['kursus.kursus'].search([]),
#         })

#     @http.route('/kursus/kursus/objects/<model("kursus.kursus"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kursus.object', {
#             'object': obj
#         })

