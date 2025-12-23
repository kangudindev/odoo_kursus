from odoo import models, fields, api

class Instruktur(models.Model):
    _name = 'cdn.instruktur'
    _description = 'Tabel Instruktur'
    _inherits = {'res.partner': 'partner_id'}
                 
    partner_id = fields.Many2one(comodel_name='res.partner', string='ID Partner', ondelete='cascade', required=True)

    keahlian_ids = fields.Many2many(comodel_name='cdn.keahlian', string='Keahlian')
    


class Keahlian(models.Model):
    _name = 'cdn.keahlian'
    _description = 'Keahlian'

    name = fields.Char(string='Keahlian', required=True)
    color = fields.Integer(string='Color Index', default=0)
    


    
