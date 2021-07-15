odoo.define('hr_attendance_geo_bms.attendance_geo', function (require) {
    "use strict";

    const attendance = require('hr_attendance.my_attendances');
    

    attendance.include({
        update_attendance(){
            var self = this;
            var options = {
                enableHighAccuracy: true,
                timeout: 5000,
                maximumAge: 0
            };
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(self.attendance_post.bind(self), self._getPositionError, options);
            }
        },
        attendance_post(position){
            var self = this;
            this._rpc({
                model: 'hr.employee',
                method: 'attendance_post',
                args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances', null, [position.coords.latitude, position.coords.longitude]],
            })
            .then(function(result) {
                if (result.action) {
                    self.do_action(result.action);
                } else if (result.warning) {
                    self.do_warn(result.warning);
                }
            });
        },
        _getPositionError(err) {
            alert("Oops, cannot get location data, try again!")
        },
    });

});
