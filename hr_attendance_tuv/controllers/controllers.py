# -*- coding: utf-8 -*-
# from odoo import http


# class HrAttendanceTuv(http.Controller):
#     @http.route('/hr_attendance_tuv/hr_attendance_tuv/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_attendance_tuv/hr_attendance_tuv/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_attendance_tuv.listing', {
#             'root': '/hr_attendance_tuv/hr_attendance_tuv',
#             'objects': http.request.env['hr_attendance_tuv.hr_attendance_tuv'].search([]),
#         })

#     @http.route('/hr_attendance_tuv/hr_attendance_tuv/objects/<model("hr_attendance_tuv.hr_attendance_tuv"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_attendance_tuv.object', {
#             'object': obj
#         })
