# -*- coding: utf-8 -*-
import base64

import werkzeug
import werkzeug.urls

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _

#from openerp import models,fields,api,_

#class hotel_reservation(models.Model):

#    _name = 'hotel.reservation'
#    _inherit = 'hotel.reservation'

#    name = fields.Char('Contact Name', size=64)
#    contact_name = fields.Char('Contact Name', size=64)
#    email_from = fields.Char('Email', size=128, help="Email address of the contact", select=1)
#    phone = fields.Char('Phone')
#    description = fields.Text('Notes')

#    _defaults = {
#        'pricelist_id': 1,
#        }

class reservations(http.Controller):

#    def generate_google_map_url(self, street, city, city_zip, country_name):
#        url = "http://maps.googleapis.com/maps/api/staticmap?center=%s&sensor=false&zoom=8&size=298x298" % werkzeug.url_quote_plus(
#            '%s, %s %s, %s' % (street, city, city_zip, country_name)
#        )
#        return url

    @http.route(['/page/website.reservations', '/page/reservations'], type='http', auth="public", website=True)
    def contact(self, **kwargs):
        values = {}
        for field in ['checkin', 'checkout', 'reservation_line', 'adults', 'children', 'contact_name', 'name', 'email_from', 'phone', 'street', 'zip', 'city', 'country_id', 'vat', 'description']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())
        return request.website.render("website.reservations", values)

    @http.route(['/page/website.rooms', '/page/rooms'], type='http', auth="public", website=True)
    def contact(self, **kwargs):
        return request.website.render("website.rooms")

    @http.route(['/page/website.rooms-double', '/page/rooms-double'], type='http', auth="public", website=True)
    def contact(self, **kwargs):
        return request.website.render("website.rooms-double")

    @http.route(['/page/website.rooms-twin', '/page/rooms-twin'], type='http', auth="public", website=True)
    def contact(self, **kwargs):
        return request.website.render("website.rooms-twin")

    @http.route(['/page/website.rooms-single', '/page/rooms-single'], type='http', auth="public", website=True)
    def contact(self, **kwargs):
        return request.website.render("website.rooms-single")



    def create_reservation(self, request, values, kwargs):
        """ Allow to be overrided """
        cr, context = request.cr, request.context
        return request.registry['hotel.reservation'].create(cr, SUPERUSER_ID, values, context=dict(context, mail_create_nosubscribe=True))

    def preRenderThanks(self, values, kwargs):
        """ Allow to be overrided """
        company = request.website.company_id
        return {
#            'google_map_url': self.generate_google_map_url(company.street, company.city, company.zip, company.country_id and company.country_id.name_get()[0][1] or ''),
            '_values': values,
            '_kwargs': kwargs,
        }

    def get_reservations_response(self, values, kwargs):
        values = self.preRenderThanks(values, kwargs)
        return request.website.render(kwargs.get("view_callback", "website_hotel.reservations_thanks"), values)

    @http.route(['/hotel/reservations'], type='http', auth="public", website=True)
    def reservations(self, **kwargs):
        def dict_to_str(title, dictvar):
            ret = "\n\n%s" % title
            for field in dictvar:
                ret += "\n%s" % field
            return ret

        _TECHNICAL = ['show_info', 'view_from', 'view_callback']  # Only use for behavior, don't stock it
#        _BLACKLIST = ['id', 'create_uid', 'create_date', 'write_uid', 'write_date', 'user_id', 'active']  # Allow in description
        _BLACKLIST = ['id', 'create_uid', 'create_date', 'write_uid', 'write_date', 'active']  # Allow in description
        _REQUIRED = ['checkin', 'checkout', 'contact_name', 'email_from', 'phone']  # Could be improved including required from model


        post_file = []  # List of file to add to ir_attachment once we have the ID
        post_description = []  # Info to add after the message
        values = {}

#        values['medium_id'] = request.registry['ir.model.data'].xmlid_to_res_id(request.cr, SUPERUSER_ID, 'hotel.hotel_medium_website')
#        values['section_id'] = request.registry['ir.model.data'].xmlid_to_res_id(request.cr, SUPERUSER_ID, 'website.salesteam_website_sales')

        for field_name, field_value in kwargs.items():
            if hasattr(field_value, 'filename'):
                post_file.append(field_value)
            elif field_name in request.registry['hotel.reservation']._fields and field_name not in _BLACKLIST:
                values[field_name] = field_value
            elif field_name not in _TECHNICAL:  # allow to add some free fields or blacklisted field like ID
                post_description.append("%s: %s" % (field_name, field_value))

        if "name" not in kwargs and values.get("contact_name"):  # if kwarg.name is empty, it's an error, we cannot copy the contact_name
            values["name"] = values.get("contact_name")
        # fields validation : Check that required field from model hotel_reservation exists
        error = set(field for field in _REQUIRED if not values.get(field))

        if error:
            values = dict(values, error=error, kwargs=kwargs.items())
            return request.website.render(kwargs.get("view_from", "website.reservations"), values)

        # description is required, so it is always already initialized
        if post_description:
            values['description'] += dict_to_str(_("Custom Fields: "), post_description)

        if kwargs.get("show_info"):
            post_description = []
            environ = request.httprequest.headers.environ
            post_description.append("%s: %s" % ("IP", environ.get("REMOTE_ADDR")))
            post_description.append("%s: %s" % ("USER_AGENT", environ.get("HTTP_USER_AGENT")))
            post_description.append("%s: %s" % ("ACCEPT_LANGUAGE", environ.get("HTTP_ACCEPT_LANGUAGE")))
            post_description.append("%s: %s" % ("REFERER", environ.get("HTTP_REFERER")))
            values['description'] += dict_to_str(_("Environ Fields: "), post_description)

        reservation_id = self.create_reservation(request, dict(values, user_id=False), kwargs)
        values.update(reservation_id=reservation_id)
        if reservation_id:
            for field_value in post_file:
                attachment_value = {
                    'name': field_value.filename,
                    'res_name': field_value.filename,
                    'res_model': 'hotel.reservation',
                    'res_id': reservation_id,
                    'datas': base64.encodestring(field_value.read()),
                    'datas_fname': field_value.filename,
                }
                request.registry['ir.attachment'].create(request.cr, SUPERUSER_ID, attachment_value, context=request.context)

        return self.get_reservations_response(values, kwargs)
