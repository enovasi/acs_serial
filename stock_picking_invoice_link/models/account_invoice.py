# Copyright 2013-15 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright 2015-2016 AvanzOSC
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2017 Jacques-Etienne Baudoux <je@bcim.be>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    picking_ids = fields.Many2many(
        comodel_name='stock.picking',
        string='Related Pickings',
        readonly=True,
        copy=False,
        help="Related pickings "
             "(only when the invoice has been generated from a sale order).",
    )


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.depends('move_line_ids')
    def _get_lots(self):
        for inv_line in self:
            inv_line.lot_ids += inv_line.mapped(
                'move_line_ids.move_line_ids.lot_id')

    move_line_ids = fields.One2many(
        comodel_name='stock.move',
        inverse_name='invoice_line_id',
        string='Related Stock Moves',
        readonly=True,
        copy=False,
        help="Related stock moves "
             "(only when the invoice has been generated from a sale order).",
    )
    lot_ids = fields.Many2many('stock.production.lot','Deliverd Serial/Lots', compute='_get_lots', help='Lot of delivered products.')
