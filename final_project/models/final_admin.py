# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api


# import res.partner customer model to add customers
class ResPartner(models.Model):
    _inherit = 'res.partner'


# import account.tax tax model to add taxes configuration menu
class adminTaxes(models.Model):
    _inherit = 'account.tax'


# create accountant report table
class AccountantReport(models.Model):
    _name = 'custom.accountant.report'
    _description = 'Admin report(accountants)'

    # custom fields
    name = fields.Char(string="Report Name", readonly=True, default='Report ID')
    accountant_id = fields.Many2one("res.partner", string="Accountant", required=True)
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    # auto created date field refers to now(the time report made)
    create_date = fields.Datetime(string='Created on', default=datetime.now(), required=True, readonly=True)
    # auto created admin field refers to the admin id who created the report
    admin = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.uid, readonly=True,
                            required=True)
    # auto created fields refers to the company id which contains the employees
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    # computed fields
    computed_profitloss_reports_names = fields.Text(compute='_compute_accountant_profitloss_reports_names', store=True)
    computed_profitloss_reports_count = fields.Integer(compute='_compute_accountant_profitloss_reports_count',
                                                       store=True)
    computed_tax_reports_names = fields.Text(compute='_compute_accountant_tax_reports_names', store=True)
    computed_tax_reports_count = fields.Integer(compute='_compute_accountant_tax_reports_count', store=True)

    # function to compute computed_profitloss_reports_names field value , its value depends on the giving fields
    @api.depends('accountant_id', 'date_from', 'date_to')
    def _compute_accountant_profitloss_reports_names(self):
        # Get the accountant and start/end dates from the data passed to the report
        accountant = self.accountant_id.user_ids.id
        start_date = self.date_from
        end_date = self.date_to

        # the list that will contain the names of the reports
        profitloss_reports_names = []

        # get all the reports from model custom.profitloss.report which specifies the requirements
        profitloss_reports = self.env['custom.profitloss.report'].search([
            ('accountant', '=', accountant),
            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date),
        ])

        # loop to append each report name into the profitloss_reports_names List
        for report in profitloss_reports:
            profitloss_reports_names.append(report.name)

        # set the list profitloss_reports_names as a value for the field computed_profitloss_reports_names
        self.computed_profitloss_reports_names = profitloss_reports_names

    # function to compute computed_profitloss_reports_count field value, its value depends on the giving fields
    @api.depends('accountant_id', 'date_from', 'date_to')
    def _compute_accountant_profitloss_reports_count(self):
        # Get the accountant and start/end dates from the data passed to the report
        accountant = self.accountant_id.user_ids.id
        start_date = self.date_from
        end_date = self.date_to

        # initialize a counter to count the profitloss report
        profitloss_reports_count = 0

        # get all the reports from model custom.profitloss.report which specifies the requirements
        profitloss_reports = self.env['custom.profitloss.report'].search([
            ('accountant', '=', accountant),
            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date),
        ])

        # loop to increase the counter by 1 for each object of model custom.profitloss.report
        for report in profitloss_reports:
            profitloss_reports_count += 1

        # set the counter profitloss_reports_count as a value for the field computed_profitloss_reports_count
        self.computed_profitloss_reports_count = profitloss_reports_count

    # function to compute computed_tax_reports_names field value, its value depends on the giving fields
    @api.depends('accountant_id', 'date_from', 'date_to')
    def _compute_accountant_tax_reports_names(self):
        # Get the accountant and start/end dates from the data passed to the report
        accountant = self.accountant_id.user_ids.id
        start_date = self.date_from
        end_date = self.date_to

        # the list that will contain the names of the reports
        tax_reports_names = []

        # get all the reports from model custom.tax.report which specifies the requirements
        profitloss_reports = self.env['custom.tax.report'].search([
            ('accountant', '=', accountant),
            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date),
        ])

        # loop to append each report name into the tax_reports_names List
        for report in profitloss_reports:
            tax_reports_names.append(report.name)

        # set the list tax_reports_names as a value for the field computed_tax_reports_names
        self.computed_tax_reports_names = tax_reports_names

    # function to compute computed_tax_reports_count field value, its value depends on the giving fields
    @api.depends('accountant_id', 'date_from', 'date_to')
    def _compute_accountant_tax_reports_count(self):
        # Get the accountant and start/end dates from the data passed to the report
        accountant = self.accountant_id.user_ids.id
        start_date = self.date_from
        end_date = self.date_to

        # initialize a counter to count the tax report
        tax_reports_count = 0

        # get all the reports from model custom.tax.report which specifies the requirements
        taxes_reports = self.env['custom.tax.report'].search([
            ('accountant', '=', accountant),
            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date),
        ])

        # loop to increase the counter by 1 for each object of model custom.profitloss.report
        for report in taxes_reports:
            tax_reports_count += 1

        # set the counter tax_reports_count as a value for the field computed_tax_reports_count
        self.computed_tax_reports_count = tax_reports_count

    # override create method to auto create the report name using predefined sequence
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('custom.accountant.sequence')
        return super(AccountantReport, self).create(vals)


# create accountant report table
class SystemReport(models.Model):
    _name = 'custom.system.report'
    _description = 'Admin report(system)'

    # custom fields
    name = fields.Char(string="Report Name", readonly=True, default='Report ID')
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    # auto created date field refers to now(the time report made)
    create_date = fields.Datetime(string='Created on', default=datetime.now(), required=True, readonly=True)
    # auto created admin field refers to the admin id who created the report
    admin = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.uid, readonly=True,
                            required=True)
    # auto created fields refers to the company id which contains the employees
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    # computed fields
    computed_taxes_names = fields.Text(compute='_compute_computed_taxes_names', store=True)
    computed_profitloss_names = fields.Text(compute='_compute_computed_profitloss_names', store=True)
    computed_taxes_count = fields.Integer(compute='_compute_computed_taxes_count', store=True)
    computed_profitloss_count = fields.Integer(compute='_compute_computed_profitloss_count', store=True)
    computed_taxes_amount = fields.Float(compute='_compute_computed_taxes_amount', store=True)

    # function to compute computed_taxes_names field value, its value depends on the giving fields
    @api.depends('date_from', 'date_to')
    def _compute_computed_taxes_names(self):
        # Get start/end dates from the data passed to the report
        start_date = self.date_from
        end_date = self.date_to

        # the list that will contain the names of the reports
        taxes_reports_names = []

        # get all the reports from model custom.tax.report which specifies the requirements
        taxes_reports = self.env['custom.tax.report'].search([
            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date),
        ])

        # loop to append each report name into the profitloss_reports_names List
        for report in taxes_reports:
            taxes_reports_names.append(report.name)

        # set the list taxes_reports_names as a value for the field computed_taxes_names
        self.computed_taxes_names = taxes_reports_names

    # function to compute computed_profitloss_names field value, its value depends on the giving fields
    @api.depends('date_from', 'date_to')
    def _compute_computed_profitloss_names(self):
        # Get start/end dates from the data passed to the report
        start_date = self.date_from
        end_date = self.date_to

        # the list that will contain the names of the reports
        profitloss_reports_names = []

        # get all the reports from model custom.profitloss.report which specifies the requirements
        profitloss_reports = self.env['custom.profitloss.report'].search([
            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date),
        ])

        # loop to append each report name into the profitloss_reports_names List
        for report in profitloss_reports:
            profitloss_reports_names.append(report.name)

        # set the list profitloss_reports_names as a value for the field computed_profitloss_names
        self.computed_profitloss_names = profitloss_reports_names

    # function to compute computed_taxes_count field value, its value depends on the giving fields
    @api.depends('date_from', 'date_to')
    def _compute_computed_taxes_count(self):
        # Get start/end dates from the data passed to the report
        start_date = self.date_from
        end_date = self.date_to

        # initialize a counter to count the taxes report
        taxes_count = 0

        # get all the reports from model custom.tax.report which specifies the requirements
        taxes_reports = self.env['custom.tax.report'].search([
            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date),
        ])

        # loop to increase the counter by 1 for each object of model custom.profitloss.report
        for report in taxes_reports:
            taxes_count += 1

        # set the counter profitloss_reports_count as a value for the field computed_profitloss_reports_count
        self.computed_taxes_count = taxes_count

    # function to compute computed_profitloss_count field value, its value depends on the giving fields
    @api.depends('date_from', 'date_to')
    def _compute_computed_profitloss_count(self):
        # Get start/end dates from the data passed to the report
        start_date = self.date_from
        end_date = self.date_to

        # initialize a counter to count the profitloss report
        profitloss_count = 0

        # get all the reports from model custom.profitloss.report which specifies the requirements
        profitloss_reports = self.env['custom.profitloss.report'].search([
            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date),
        ])

        # loop to increase the counter by 1 for each object of model custom.profitloss.report
        for report in profitloss_reports:
            profitloss_count += 1

        # set the counter profitloss_count as a value for the field computed_profitloss_count
        self.computed_profitloss_count = profitloss_count

    # function to compute computed_taxes_amount field value, its value depends on the giving fields
    @api.depends('date_from', 'date_to')
    def _compute_computed_taxes_amount(self):
        # Get start/end dates from the data passed to the report
        start_date = self.date_from
        end_date = self.date_to

        # initialize a counter to count the taxes report
        taxes_amount = 0

        # get all the reports from model account.move which specifies the requirements
        invoices = self.env['account.move'].search([
            ('date', '>=', start_date),
            ('date', '<=', end_date),
            ('move_type', '=', 'out_invoice')
        ])

        # loop to increase the counter by adding each invoices tax to the counter taxes_amount
        for report in invoices:
            taxes_amount += report.amount_tax

        # set the counter taxes_amount as a value for the field computed_taxes_amount
        self.computed_taxes_amount = taxes_amount

    # override create method to auto create the report name using predefined sequence
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('custom.system.sequence')
        return super(SystemReport, self).create(vals)
