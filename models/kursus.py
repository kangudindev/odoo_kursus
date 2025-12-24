from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Kursus (models.Model):
    _name = 'cdn.kursus'
    _description = 'Tabel Kursus'

    name = fields.Char(string='Nama Kursus', required=True)
    description = fields.Text(string='Deskripsi')
    user_id = fields.Many2one(comodel_name='res.users', string='Penanggung Jawab')
    session_line = fields.One2many(comodel_name='cdn.sesi.kursus', inverse_name='kursus_id', string='Sesi')
    produk_ids = fields.Many2many(comodel_name='product.product', string='Konsumsi', domain=[('type', 'in', ('consu', 'product'))])
    produk_kursus_id = fields.Many2one(comodel_name='product.product', string='Produk Kursus', domain=[('is_kursus_product', '=', True)])
    biaya_konsumsi = fields.Float(string='Biaya Konsumsi', compute='_compute_biaya_konsumsi')
    harga_kursus = fields.Float(related='produk_kursus_id.lst_price', string='Harga Kursus')
    # currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    color = fields.Integer('Color Index', default=0)
    progress = fields.Float( string='Progress', compute='_compute_progress', store=True)

    @api.depends('session_line.state')
    def _compute_progress(self):
        for kursus in self:
            total_sesi = len(kursus.session_line)
            if total_sesi == 0:
                kursus.progress = 0
            else:
                total_score = 0
                for sesi in kursus.session_line:
                    if sesi.state == 'draft':
                        total_score += 0
                    elif sesi.state == 'confirm':
                        total_score += 0.5 
                    elif sesi.state == 'done':
                        total_score += 1 
                kursus.progress = (total_score / total_sesi) * 100



    @api.depends('produk_ids')
    def _compute_biaya_konsumsi(self):
        for record in self:
            record.biaya_konsumsi = sum(record.produk_ids.mapped('lst_price'))




class SesiKursus(models.Model):
    _name = 'cdn.sesi.kursus'
    _description = 'Tabel Sesi Kursus'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nama Sesi', required=True, tracking=True)
    kursus_id = fields.Many2one(comodel_name='cdn.kursus', string='Nama Kursus', required=True, ondelete='cascade')
    start_date = fields.Date(string='Tgl Mulai', required=True, tracking=True)
    duration = fields.Float(string='Durasi', required=True, tracking=True)
    seats = fields.Integer(string='Peserta', compute='_compute_seats', tracking=True)
    peserta_ids = fields.Many2many(comodel_name='cdn.peserta', string='ID Peserta', ondelete='cascade', required=True)
    instruktur_id = fields.Many2one(comodel_name='cdn.instruktur', string='ID Instruktur', ondelete='cascade')
    no_hp = fields.Char(string='No HP',related="instruktur_id.mobile")
    email = fields.Char(string='Email',related="instruktur_id.email")
    jenis_kelamin = fields.Selection(related="instruktur_id.jenis_kelamin")
    jml_peserta = fields.Integer(string='Jumlah Peserta')
    state = fields.Selection([ ('draft', 'Draft'), ('confirm', 'Sedang Berlangsung'), ('done', 'Selesai')], string='Status', default='draft', tracking=True)


    @api.depends ('peserta_ids')
    def _compute_seats(self):
        for record in self:
            record.seats= len(record.peserta_ids)
    

    def action_reset(self):
        for record in self:
            record.state = 'draft'

    def action_confirm(self):
         for record in self:
            if not record.instruktur_id:
                raise ValidationError("Instruktur harus di isi, tidak boleh kosong !")
            record.state = 'confirm' if record.state == 'draft' else record.state

    def action_done(self):
        for record in self:
            record.state = 'done' if record.state == 'confirm' else record.state

    def action_print_session(self):
        return self.env.ref('kursus.report_sesi_kursus_pdf_action').report_action(self)   





class SesiKursuInherit(models.Model):
    _inherit = 'cdn.sesi.kursus'


    keterangan = fields.Char(string='Keterangan')


    def action_confirm(self):
        self.keterangan='hasil inherit'
        # return super(SesiKursuInherit, self).action_confirm()
        return super().action_confirm()
