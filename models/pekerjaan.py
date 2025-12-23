from odoo import models, fields, api, _


class Pekerjaan(models.Model):
    _name = 'cdn.pekerjaan'
    _description = 'Tabel Pekerjaan'

    name = fields.Char(string='Nama Pekerjaan')
    keterangan = fields.Char(string='Keterangan')

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            # self.name = self.name.upper()
            # self.name = self.name.lower()
            self.name = self.name.capital()
    
    