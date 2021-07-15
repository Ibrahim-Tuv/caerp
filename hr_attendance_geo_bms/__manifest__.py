{
    'name': 'Hr Attendance Geo BMS',
    'summary': """
                Melakukan pencatatan lokasi ketika Check In dan Check Out, serta memberikan informasi google maps atas koordinat yang didapat
                """,
    'version': '1',
    'author': 'BMS',
    'website': 'beringinsedaya.tech',
    'depends': [
        'hr_attendance',
    ],
    'data': [
        'views/assets.xml',
        'views/hr_attendance_views.xml'
    ]
}
