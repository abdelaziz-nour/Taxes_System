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
    # auto created date field refers to now(the time report made)
    create_date = fields.Datetime(string='Created on', default=datetime.now(), required=True, readonly=True)
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
    computed_names = fields.Text(compute='_compute_computed_names', store=True)
    computed_amount = fields.Text(compute='_compute_computed_amount', store=True)
    computed_tax = fields.Text(compute='_compute_computed_tax', store=True)
    computed_total = fields.Integer(compute='_compute_computed_total', store=True)

    # function to compute computed_names field value , its value depends on the giving fields
    @api.depends('customer_id', 'date_from', 'date_to', 'target_move')
    def _compute_computed_names(self):
        # Get the customer , start/end dates and the target moves from the data passed to the report
        customer = self.customer_id
        date_from = self.date_from
        date_to = self.date_to
        target_move = self.target_move

        # check if the value of target move is  posted to get only posted target move
        if target_move == "posted":

            # get all the objects from model account.move which specifies the requirements
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ("state", "=", target_move),
                ('move_type', '=', 'out_invoice')
            ])

        # otherwise get all invoices no matter what is the target move
        else:
            # get all the objects from model account.move which specifies the requirements
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ('move_type', '=', 'out_invoice')
            ])

        # initialize invoices_names List which will contains the invoices names
        invoices_names = []

        # loop to append each report name into the invoices_names List
        for invoice in invoices:
            invoices_names.append(invoice.name)

        # set the list invoices_names as a value for the field computed_names
        self.computed_names = invoices_names

    # function to compute computed_amount field value , its value depends on the giving fields
    @api.depends('customer_id', 'date_from', 'date_to', 'target_move')
    def _compute_computed_amount(self):
        # Get the customer , start/end dates and the target moves from the data passed to the report
        customer = self.customer_id
        date_from = self.date_from
        date_to = self.date_to
        target_move = self.target_move

        # check if the value of target move is  posted to get only posted target move
        if target_move == "posted":
            # get all the objects from model account.move which specifies the requirements
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ("state", "=", target_move),
                ('move_type', '=', 'out_invoice')
            ])

        # otherwise get all invoices no matter what is the target move
        else:
            # get all the objects from model account.move which specifies the requirements
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ('move_type', '=', 'out_invoice')
            ])
        # the list that will contain the invoices amounts
        invoices_amount = []

        # loop to append each invoice amount into the invoices_amount List
        for invoice in invoices:
            invoices_amount.append(invoice.amount_untaxed)

        # set the list invoices_amount as a value for the field computed_amount
        self.computed_amount = invoices_amount

    # function to compute computed_tax field value , its value depends on the giving fields
    @api.depends('customer_id', 'date_from', 'date_to', 'target_move')
    def _compute_computed_tax(self):
        # Get the customer , start/end dates and the target moves from the data passed to the report
        customer = self.customer_id
        date_from = self.date_from
        date_to = self.date_to
        target_move = self.target_move
        # check if the value of target move is  posted to get only posted target move
        if target_move == "posted":

            # get all the objects from model account.move which specifies the requirements
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ("state", "=", target_move),
                ('move_type', '=', 'out_invoice')
            ])

        # otherwise get all invoices no matter what is the target move
        else:

            # get all the objects from model account.move which specifies the requirements
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ('move_type', '=', 'out_invoice')
            ])

        # the list that will contain the invoices taxes
        invoices_tax = []

        # loop to append each invoice tax into the invoices_tax List
        for invoice in invoices:
            invoices_tax.append(invoice.amount_tax)

        # set the list invoices_tax as a value for the field computed_tax
        self.computed_tax = invoices_tax

    # function to compute computed_total field value , its value depends on the giving fields
    @api.depends('customer_id', 'date_from', 'date_to', 'target_move')
    def _compute_computed_total(self):
        # Get the customer , start/end dates and the target moves from the data passed to the report
        customer = self.customer_id
        date_from = self.date_from
        date_to = self.date_to
        target_move = self.target_move

        # check if the value of target move is  posted to get only posted target move
        if target_move == "posted":
            # get all the objects from model account.move which specifies the requirements
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ("state", "=", target_move),
                ('move_type', '=', 'out_invoice')
            ])

        # otherwise get all invoices no matter what is the target move
        else:
            # get all the objects from model account.move which specifies the requirements
            invoices = self.env["account.move"].search([
                ("partner_id", "=", customer.id),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ('move_type', '=', 'out_invoice')
            ])
        # initialize total amount counter
        total_amount = 0

        # loop to increase the counter by adding each invoices amount to the counter total_amount
        for invoice in invoices:
            total_amount += invoice.amount_total

        # set the counter total_amount as a value for the field computed_total
        self.computed_total = total_amount

    # override create method to auto create the report name using predefined sequence
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('custom.tax.sequence')
        return super(CustomTaxReport, self).create(vals)

