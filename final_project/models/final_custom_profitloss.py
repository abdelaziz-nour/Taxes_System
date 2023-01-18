# Import the necessary modules and libraries
from odoo import api, fields, models
from datetime import datetime


# Define the custom profit/loss report model
class ProfitLossReport(models.Model):
    _name = 'custom.profitloss.report'
    _description = 'Profit and Loss Report'

    # Define the fields of the model
    name = fields.Char(string="Report Name", readonly=True, default='Report ID')
    customer_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True)
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    # auto created date field refers to now(the time report made)
    create_date = fields.Datetime(string='Created on', default=datetime.now(), required=True, readonly=True, )
    # auto created admin field refers to the accountant id who created the report
    accountant = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.uid, readonly=True,
                                 required=True)
    # auto created fields refers to the company id which contains the employees
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    journal_ids = fields.Many2many('account.journal', string='Journals', required=True,
                                   default=lambda self: self.env['account.journal'].search(
                                       [('company_id', '=', self.company_id.id)]))
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('all', 'All Entries'),
                                    ], string='Target Moves', required=True, default='posted')
    # computed fields
    computed_revenue = fields.Integer(compute='_compute_computed_revenue', store=True)
    computed_costs = fields.Integer(compute='_compute_computed_costs', store=True)
    computed_profitloss = fields.Integer(compute='_compute_computed_profitloss', store=True)

    # function to compute computed_revenue field value , its value depends on the giving fields
    @api.depends('customer_id', 'date_from', 'date_to', 'target_move')
    def _compute_computed_revenue(self):
        # Get the customer , start/end dates and the target moves from the data passed to the report
        customer = self.customer_id
        date_from = self.date_from
        date_to = self.date_to
        target_move = self.target_move

        # check if the value of target move is  posted to get only posted target move
        if target_move == "posted":
            # get all the objects from model account.move which specifies the requirements
            invoices = self.env['account.move'].search([
                ('partner_id', '=', customer.id),
                ('date', '>=', date_from),
                ('date', '<=', date_to),
                ("state", "=", target_move),
                ('move_type', 'in', ['out_invoice', 'in_invoice'])
            ])

        # otherwise get all invoices no matter what is the target move
        else:
            # get all the objects from model account.move which specifies the requirements
            invoices = self.env['account.move'].search([
                ('partner_id', '=', customer.id),
                ('date', '>=', date_from),
                ('date', '<=', date_to),
                ('move_type', 'in', ['out_invoice', 'in_invoice'])
            ])

        # initialize revenue counter
        total_revenue = 0

        # get the amount of the invoices and add it to the counter total_revenue
        # out_invoice is the customers invoices (positive amount)
        for invoice in invoices:
            for line in invoice.invoice_line_ids:
                if invoice.move_type == 'out_invoice':
                    total_revenue += line.price_subtotal

        # set the counter total_revenue as a value for the field computed_revenue
        self.computed_revenue = total_revenue

    # function to compute computed_costs field value , its value depends on the giving fields
    @api.depends('customer_id', 'date_from', 'date_to', 'target_move')
    def _compute_computed_costs(self):
        # Get the customer , start/end dates and the target moves from the data passed to the report
        customer = self.customer_id
        date_from = self.date_from
        date_to = self.date_to
        target_move = self.target_move

        # check if the value of target move is  posted to get only posted target move
        if target_move == "posted":
            # get all the objects from model account.move which specifies the requirements
            invoices = self.env['account.move'].search([
                ('partner_id', '=', customer.id),
                ('date', '>=', date_from),
                ('date', '<=', date_to),
                ("state", "=", target_move),
                ('move_type', 'in', ['out_invoice', 'in_invoice'])
            ])

        # otherwise get all invoices no matter what is the target move
        else:
            # get all the objects from model account.move which specifies the requirements
            invoices = self.env['account.move'].search([
                ('partner_id', '=', customer.id),
                ('date', '>=', date_from),
                ('date', '<=', date_to),
                ('move_type', 'in', ['out_invoice', 'in_invoice'])
            ])

        # initialize costs counter
        total_costs = 0

        # get the amount of the invoices and add it to the counter total_costs
        # in_invoice is the customers invoices (negative amount)
        for invoice in invoices:
            for line in invoice.invoice_line_ids:
                if invoice.move_type == 'in_invoice':
                    total_costs += line.price_subtotal

        # set the counter total_costs as a value for the field computed_costs
        self.computed_costs = total_costs

    # function to compute computed_profitloss field value , its value depends on the giving fields
    @api.depends('computed_revenue', 'computed_costs')
    def _compute_computed_profitloss(self):
        # get the revenue and the costs from the computed fields
        revenue = self.computed_revenue
        costs = self.computed_costs

        # account the profit and loss value
        self.computed_profitloss = revenue - costs

    # override create method to auto create the report name using predefined sequence
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('custom.profitloss.sequence')
        return super(ProfitLossReport, self).create(vals)
