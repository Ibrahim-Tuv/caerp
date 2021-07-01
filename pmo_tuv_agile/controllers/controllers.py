# -*- coding: utf-8 -*-
# from odoo import http


# class PmoTuvAgile(http.Controller):
#     @http.route('/pmo_tuv_agile/pmo_tuv_agile/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pmo_tuv_agile/pmo_tuv_agile/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pmo_tuv_agile.listing', {
#             'root': '/pmo_tuv_agile/pmo_tuv_agile',
#             'objects': http.request.env['pmo_tuv_agile.pmo_tuv_agile'].search([]),
#         })

#     @http.route('/pmo_tuv_agile/pmo_tuv_agile/objects/<model("pmo_tuv_agile.pmo_tuv_agile"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pmo_tuv_agile.object', {
#             'object': obj
#         })
