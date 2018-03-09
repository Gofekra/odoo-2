# coding:utf-8


from odoo import fields,models

class hm_partner(models.Model):
        _inherit='res.partner'


        city=fields.Many2one('hm.city',string='city')
        street2=fields.Many2one('hm.district',string='district')


        def _display_self(self, without_company=False):

            '''
            The purpose of this function is to build and return an self formatted accordingly to the
            standards of the country where it belongs.

            :param self: browse record of the res.partner to format
            :returns: the self formatted in a display that fit its country habits (or the default ones
                if not country is specified)
            :rtype: string
            '''

            # get the information that will be injected into the display format
            # get the self format
            self_format = self.country_id.self_format or \
              "%(street)s\n%(street2)s\n%(city)s %(state_code)s %(zip)s\n%(country_name)s"
            args = {
            'state_code': self.state_id.code or '',
            'state_name': self.state_id.name or '',
            'country_code': self.country_id.code or '',
            'country_name': self.country_id.name or '',
            'company_name': self.parent_name or '',
            'mobile':self.mobile or '',
            }
            for field in self._self_fields():
                args[field] = getattr(self, field) or ''
            if without_company:
                args['company_name'] = ''
            elif self.parent_id:
                self_format = '%(company_name)s\n' + self_format
            args['city']=self.city.name or ''
            return self_format % args