from odoo import models, fields, api

class DaftarHadir(models.Model):
    _name = 'cdn.daftar_hadir'
    _description = 'Daftar Hadir'
    _rec_name = 'kursus_id'


    tanggal = fields.Date(string='Tanggal', default=fields.Date.today, required=True)
    kursus_id = fields.Many2one('cdn.kursus', string='Kursus', required=True)
    sesi_kursus_id = fields.Many2one('cdn.sesi.kursus', string='Sesi Kursus', required=True)
    daftar_hadir_ids = fields.One2many('cdn.daftar_hadir_list', 'daftar_hadir_id', string='Daftar Siswa')
    instruktur_id = fields.Many2one('cdn.instruktur', string='Instruktur', related='sesi_kursus_id.instruktur_id', readonly=True)
    no_hp = fields.Char(string='No HP', related="instruktur_id.mobile", readonly=True)
    email = fields.Char(string='Email', related="instruktur_id.email", readonly=True)
    total_peserta = fields.Integer(string='Total Peserta', readonly=True)
    state = fields.Selection(string='Status', selection=[('draft', 'Draft'), ('confirm', 'Konfirmasi'), ('done', 'Selesai')], default='draft')
    jml_hadir = fields.Integer(compute='_compute_jumlah_presensi', store=True)
    jml_sakit = fields.Integer(compute='_compute_jumlah_presensi', store=True)
    jml_izin  = fields.Integer(compute='_compute_jumlah_presensi', store=True)
    jml_alpha = fields.Integer(compute='_compute_jumlah_presensi', store=True)

    
    @api.onchange('kursus_id', 'sesi_kursus_id')
    def _onchange_sesi_kursus_id(self):
        if self.kursus_id and self.sesi_kursus_id:
            self.daftar_hadir_ids = [(5, 0, 0)]
            
            pendaftaran_records = self.env['cdn.pendaftaran'].search([
                ('kursus_id', '=', self.kursus_id.id),
                ('state', '=', 'confirm')
            ])
            line = []
            for reg in pendaftaran_records:
                line.append((0, 0, {
                    'peserta_id': reg.pendaftar_id.id,
                    'presensi': 'h',
                }))
            
            self.daftar_hadir_ids = line
            self.total_peserta = len(pendaftaran_records)

    def action_confirm(self):
        for record in self:
            record.state = 'confirm' if record.state == 'draft' else record.state

    def action_reset(self):
        for record in self:
            record.state = 'draft'

    
    @api.depends('daftar_hadir_ids.presensi')
    def _compute_jumlah_presensi(self):
        for record in self:
            record.jml_hadir = len(record.daftar_hadir_ids.filtered(lambda x: x.presensi == 'h'))
            record.jml_sakit = len(record.daftar_hadir_ids.filtered(lambda x: x.presensi == 's'))
            record.jml_izin  = len(record.daftar_hadir_ids.filtered(lambda x: x.presensi == 'i'))
            record.jml_alpha = len(record.daftar_hadir_ids.filtered(lambda x: x.presensi == 'a'))

    


class DaftarHadirList(models.Model):
    _name = "cdn.daftar_hadir_list"
    _description = "Detail Daftar Hadir"

    daftar_hadir_id = fields.Many2one('cdn.daftar_hadir', string='Daftar Hadir')
    peserta_id = fields.Many2one('cdn.peserta', string='Peserta')
    jenis_kelamin = fields.Selection(string='Jenis Kelamin', related="peserta_id.jenis_kelamin", readonly=True)
    no_hp = fields.Char(string='No. HP', related="peserta_id.mobile", readonly=True)
    presensi = fields.Selection([ ('a', 'Alpha'), ('s', 'Sakit'), ('i', 'Izin'), ('h', 'Hadir')], string='Presensi', default='h')
    