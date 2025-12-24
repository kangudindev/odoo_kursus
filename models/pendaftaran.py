from odoo import models, fields, api

class Pendaftaran(models.Model):
    _name = 'cdn.pendaftaran'
    _description = 'Tabel Pendaftaran'

    name = fields.Char(string='Nomor Pendaftaran', readonly=True)
    tanggal = fields.Date(string='Tanggal', default=fields.Date.today, required=True)
    pendaftar_id = fields.Many2one(comodel_name='cdn.peserta', string='Pendaftar', required=True)
    jenis_kelamin = fields.Selection(string='Jenis Kelamin', related='pendaftar_id.jenis_kelamin', readonly=True)
    no_hp = fields.Char(string='No. HP', related='pendaftar_id.mobile', readonly=True)
    kursus_id = fields.Many2one(comodel_name='cdn.kursus', string='Kursus', required=True)
    harga_kursus = fields.Float(string='Harga Kursus', related='kursus_id.harga_kursus', readonly=True)
    # currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection(string='Status', selection=[('draft', 'Draft'), ('confirm', 'Konfirmasi'), ('done', 'Selesai')], default='draft')
    invoice_id = fields.Many2one(comodel_name='account.move', string='No. Tagihan', readonly=True)
    # status_pembayaran = fields.Selection(string='Status Pembayaran', related='invoice_id.status_in_payment', store=True)
    status_pembayaran = fields.Selection(string='Status Pembayaran', related='invoice_id.payment_state', store=True)
    

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('seq_pendaftaran')
        return super(Pendaftaran, self).create(vals)


    def action_reset(self):
        for record in self:
            record.state = 'draft'

    def action_confirm(self):
        for record in self:
            record.state = 'confirm' if record.state == 'draft' else record.state

    def action_create_invoice(self):
        for record in self:
            Invoice = self.env['account.move'].create({
                'partner_id': record.pendaftar_id.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_date': record.tanggal,
                'invoice_line_ids': [(0, 0, {
                    'name': record.kursus_id.name,
                    'product_id': record.kursus_id.produk_kursus_id.id,
                    'quantity': 1,
                    'price_unit': record.harga_kursus,
                })],
            })
            record.invoice_id = Invoice.id
            Invoice.action_post()