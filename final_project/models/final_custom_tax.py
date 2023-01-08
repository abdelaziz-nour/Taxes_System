# Import the required modules
from datetime import datetime
from odoo import models, fields, api


# Define the custom tax report model
class CustomTaxReport(models.Model):
    _name = "custom.tax.report"

    # Define the fields of the model
    name = fields.Char(string="Report Name", readonly=True, default='Report ID')
    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True)
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)

    create_date = fields.Datetime(string='Created on', default=datetime.now(), required=True, readonly=True, )
    accountant = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.uid, readonly=True,
                                 required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    journal_ids = fields.Many2many('account.journal', string='Journals', required=True,
                                   default=lambda self: self.env['account.journal'].search(
                                       [('company_id', '=', self.company_id.id)]))
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('all', 'All Entries'),
                                    ], string='Target Moves', required=True, default='posted')
    computed_names = fields.Text(compute='_compute_computed_names', store=True)
    computed_amount = fields.Text(compute='_compute_computed_amount', store=True)
    computed_tax = fields.Text(compute='_compute_computed_tax', store=True)
    computed_total = fields.Integer(compute='_compute_computed_total', store=True)

    @api.depends('customer_id', 'date_from', 'date_to', 'target_move')
    def _compute_computed_names(self):
        customer = self.customer_id
        date_from = self.date_from
        date_to = self.date_to
        target_move = self.target_move
        if target_move == "posted":
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ("state", "=", target_move),
                ('move_type', '=', 'out_invoice')
            ])
        else:
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ('move_type', '=', 'out_invoice')
            ])

        invoices_names = []

        for invoice in invoices:
            invoices_names.append(invoice.name)

        self.computed_names = invoices_names

    @api.depends('customer_id', 'date_from', 'date_to', 'target_move')
    def _compute_computed_amount(self):
        customer = self.customer_id
        date_from = self.date_from
        date_to = self.date_to
        target_move = self.target_move

        if target_move == "posted":
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ("state", "=", target_move),
                ('move_type', '=', 'out_invoice')
            ])
        else:
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ('move_type', '=', 'out_invoice')
            ])

        invoices_amount = []
        for invoice in invoices:
            invoices_amount.append(invoice.amount_untaxed)

        self.computed_amount = invoices_amount

    @api.depends('customer_id', 'date_from', 'date_to', 'target_move')
    def _compute_computed_tax(self):
        customer = self.customer_id
        date_from = self.date_from
        date_to = self.date_to
        target_move = self.target_move

        if target_move == "posted":
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ("state", "=", target_move),
                ('move_type', '=', 'out_invoice')
            ])
        else:
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ('move_type', '=', 'out_invoice')
            ])

        invoices_tax = []

        for invoice in invoices:
            invoices_tax.append(invoice.amount_tax)

        self.computed_tax = invoices_tax

    @api.depends('customer_id', 'date_from', 'date_to', 'target_move')
    def _compute_computed_total(self):
        customer = self.customer_id
        date_from = self.date_from
        date_to = self.date_to
        target_move = self.target_move

        if target_move == "posted":
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ("state", "=", target_move),
                ('move_type', '=', 'out_invoice')
            ])
        else:
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ('move_type', '=', 'out_invoice')
            ])

        total_amount = 0

        for invoice in invoices:
            total_amount += invoice.amount_total

        self.computed_total = total_amount

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('custom.tax.sequence')
        return super(CustomTaxReport, self).create(vals)

    # def generate_report(self):
    #     customer = self.customer_id
    #     date_from = self.date_from
    #     date_to = self.date_to
    #     target_move = self.target_move
    #
    #     if target_move == "posted":
    #         invoices = self.env["account.move"].search([
    #             ("partner_id", "=", customer.id),
    #             ("date", ">=", date_from),
    #             ("date", "<=", date_to),
    #             ("state", "=", target_move)
    #         ])
    #     else:
    #         invoices = self.env["account.move"].search([
    #             ("partner_id", "=", customer.id),
    #             ("date", ">=", date_from),
    #             ("date", "<=", date_to)])
    #     print('ttt')
    #     print(target_move)
    #     invoices_names = []
    #     invoices_untaxed = []
    #     invoices_taxes = []
    #     invoices_total = []

    # get invoices amount and date
    # total_amount = 0
    # for invoice in invoices:
    #     invoices_names.append(invoice.name)
    #     invoices_untaxed.append(invoice.amount_untaxed)
    #     invoices_taxes.append(invoice.amount_tax)
    #     invoices_total.append(invoice.amount_total)
    #     total_amount += invoice.amount_total
    # print('create Date :')
    # print(invoice.date)
    # print('created by')
    # print(invoice.invoice_user_id.display_name)
    # print('Invoice Name')
    # print(invoice.name)
    # print('Invoice amount_total')
    # print(invoice.amount_untaxed)
    # print('Invoice amount_tax')
    # print(invoice.amount_tax)
    # print('------------')

    # print('total :')
    # print(total_amount)

    # data = {
    #     'invoices names': invoices_names,
    #     'invoices untaxed': invoices_untaxed,
    #     'invoices taxes': invoices_taxes,
    #     'invoices total': invoices_total,
    #     'total amount': total_amount
    #
    # }
    # nm = self.env["custom.tax.report"].search([])
    # #print(invoices_names)
    # print(nm)
    # print(self.computed_names)
    # print(self.computed_amount)
    # print(self.computed_tax)
    # print(self.computed_total)
