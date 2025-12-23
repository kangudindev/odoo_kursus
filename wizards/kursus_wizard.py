from odoo import models, fields, api
from odoo.exceptions import UserError


class KursusWizard(models.TransientModel):
    _name = 'cdn.kursus.wizard'
    _description = 'Wizard Kursus'


    def _default_sesi(self):
        return self.env['cdn.sesi.kursus'].browse(self._context.get('active_ids'))
    
    session_id = fields.Many2one(comodel_name='cdn.sesi.kursus', string='Sesi Kursus', default=_default_sesi)
    session_ids = fields.Many2many(comodel_name='cdn.sesi.kursus', string='Multi Sesi Training', default=_default_sesi)
    peserta_ids = fields.Many2many(comodel_name='cdn.peserta', string='Peserta Training')


    def action_add_peserta(self):
        if self.session_id.state == 'done':
            raise UserError("Tidak dapat menambahkan Peserta, Sesi Kursus sudah Selesai !")
        self.session_id.peserta_ids |= self.peserta_ids

    def action_add_many_peserta(self):
        for session in self.session_ids:
            if session.state != 'done':
                session.peserta_ids |= self.peserta_ids
