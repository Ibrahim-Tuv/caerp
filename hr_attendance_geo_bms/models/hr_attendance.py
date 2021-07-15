from odoo import fields, models

class HrAttendance(models.Model):
    _inherit = "hr.attendance"
    check_in_latitude = fields.Char( "CheckIn Latitude",readonly=True)
    check_in_longitude = fields.Char( "CheckIn Longitude",readonly=True)
    check_in_maps = fields.Char("Link Gmaps CheckIn", readonly=True)
    check_out_latitude = fields.Char( "CheckOut Latitude",readonly=True)
    check_out_longitude = fields.Char( "CheckOut Longitude",readonly=True)
    check_out_maps = fields.Char("Link Gmaps CheckOut", readonly=True)
