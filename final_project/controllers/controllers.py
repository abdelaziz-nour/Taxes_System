# -*- coding: utf-8 -*-
# from odoo import http


# class FinalProject(http.Controller):
#     @http.route('/final_project/final_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/final_project/final_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('final_project.listing', {
#             'root': '/final_project/final_project',
#             'objects': http.request.env['final_project.final_project'].search([]),
#         })

#     @http.route('/final_project/final_project/objects/<model("final_project.final_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('final_project.object', {
#             'object': obj
#         })
