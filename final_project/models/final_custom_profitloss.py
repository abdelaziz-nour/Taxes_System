# Import the necessary modules and libraries
from odoo import api, fields, models
from datetime import datetime

class ProfitLossReport(models.Model):
    _name = 'custom.profitloss.report'
    _description = 'Profit and Loss Report'

    name = fields.Char(string="Report Name", readonly=True,default='Report ID')
    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True)
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)

    create_date = fields.Datetime(string='Created on', default=datetime.now(), required=True, readonly=True,)
    accountant = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.uid, readonly=True, required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    journal_ids = fields.Many2many('account.journal', string='Journals', required=True, default=lambda self: self.env['account.journal'].search([('company_id', '=', self.company_id.id)]))
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('all', 'All Entries'),
                                    ], string='Target Moves', required=True, default='posted')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('custom.profitloss.sequence')
        return super(ProfitLossReport, self).create(vals)

    def get_report_values(self):
        # Get the customer and start/end dates from the data passed to the report
        customer = self.customer_id
        start_date = self.date_from
        end_date = self.date_to
        accountant = self.accountant
        # Get a list of all invoices for the customer within the specified date range
        invoices = self.env['account.move'].search([
            ('partner_id', '=', customer.id),
            ('date', '>=', start_date),
            ('date', '<=', end_date),
            ('move_type', 'in', ['out_invoice', 'in_invoice'])
        ])

        # Calculate the total revenue and total costs for the customer
        total_revenue = 0
        total_costs = 0
        for invoice in invoices:
            for line in invoice.invoice_line_ids:
                if invoice.move_type == 'out_invoice':
                    total_revenue += line.price_subtotal
                else:
                    total_costs += line.price_subtotal

        # Calculate the profit/loss for the customer
        profit_loss = total_revenue - total_costs

        # Return the report values

        print('customer')
        print(customer.display_name)
        print('start_date')
        print(start_date)
        print('end_date')
        print(end_date)
        print('total_revenue')
        print(total_revenue)
        print('total_costs')
        print(total_costs)
        print('profit_loss')
        print(profit_loss)
        print('created by')
        print(accountant.id)

