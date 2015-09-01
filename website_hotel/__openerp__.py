# -*- coding: utf-8 -*-

{
    'name': 'Online Reservation',
    'category': 'Website',
    'summary': 'Hotel reservations',
    'website': 'http://www.communities.pt',
    'version': '1.0',
    'description': """
Online Hotel Reservation
        """,
    'author': 'Communities - Comunicações',
    'depends': ['website_partner', 'hotel_reservation'],
    'data': [
        'data/website_hotel_data.xml',
        'views/website_hotel.xml',
        'views/website_hotel_rooms.xml',
        'views/website_hotel_rooms_double.xml',
        'views/website_hotel_rooms_single.xml',
        'views/website_hotel_rooms_twin.xml',
    ],
    'installable': True,
    'auto_install': False,
}
