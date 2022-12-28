# Import the required modules
from datetime import datetime
from odoo import models, fields, api


# Define the custom tax report model
class CustomTaxReport(models.Model):
    _name = "custom.tax.report"

    # Define the fields of the model
    name = fields.Char(string="Report Name", readonly=True,default='Report ID')
    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True)
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)

    create_date = fields.Datetime(string='Created on', default=datetime.now(), required=True, readonly=True,)
    accountant = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.uid, readonly=True, required=True )
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    journal_ids = fields.Many2many('account.journal', string='Journals', required=True, default=lambda self: self.env['account.journal'].search([('company_id', '=', self.company_id.id)]))
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('all', 'All Entries'),
                                    ], string='Target Moves', required=True, default='posted')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('custom.tax.sequence')
        return super(CustomTaxReport, self).create(vals)

    # Define the method that generates the tax report
    def generate_report(self):
        # Get the values from the form
        customer = self.customer_id
        date_from = self.date_from
        date_to = self.date_to

        # Get the invoices of the customer for the specified date range
        invoices = self.env["account.move"].search([
            ("partner_id", "=", customer.id),
            ("date", ">=", date_from),
            ("date", "<=", date_to)
        ])
        print(invoices)

        # get invoices amount and date
        total_amount = 0
        for invoice in invoices:
            total_amount += invoice.amount_total
            print('create Date :')
            print(invoice.date)
            print('created by')
            print(invoice.invoice_user_id.display_name)
            print('------------')
        print('total :')
        print(total_amount)











