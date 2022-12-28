# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api


class my_admin(models.Model):
    _name = 'final.admin'
    _description = 'final admin'

class ResPartner(models.Model):
    _inherit = 'res.partner'

class adminTaxes(models.Model):
    _inherit = 'account.tax'

class AccountantReport(models.Model):
    _name = 'custom.accountant.report'
    _description = 'Admin report(accountants)'

    name = fields.Char(string="Report Name", readonly=True, default='Report ID')
    accountant_id = fields.Many2one("res.partner", string="Accountant", required=True)
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    create_date = fields.Datetime(string='Created on', default=datetime.now(), required=True, readonly=True,)
    admin = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.uid, readonly=True, required=True )
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('custom.accountant.sequence')
        return super(AccountantReport, self).create(vals)

    def get_accountant_reports(self):
        # Get the customer and start/end dates from the data passed to the report
        accountant = self.accountant_id.user_ids.id
        start_date = self.date_from
        end_date = self.date_to
        profitloss_reports_count = 0
        tax_reports_count = 0

        profitloss_reports = self.env['custom.profitloss.report'].search([

            ('accountant', '=', accountant),
            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date),
        ])

        taxes_reports = self.env['custom.tax.report'].search([
            ('accountant', '=', accountant),
            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date),
        ])

        for report in profitloss_reports:
            print(report.name)
            profitloss_reports_count += 1
        print(profitloss_reports_count)
        for report in taxes_reports:
            print(report.name)
            tax_reports_count += 1
        print(tax_reports_count)

class SystemReport(models.Model):
    _name = 'custom.system.report'
    _description = 'Admin report(system)'

    name = fields.Char(string="Report Name", readonly=True,default='Report ID')
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    create_date = fields.Datetime(string='Created on', default=datetime.now(), required=True, readonly=True,)
    accountant = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.uid, readonly=True, required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('custom.system.sequence')
        return super(SystemReport, self).create(vals)

    def get_system_reports(self):
        # Get the customer and start/end dates from the data passed to the report
        #accountant = self.accountant_id.user_ids.id
        start_date = self.date_from
        end_date = self.date_to
        profitloss_reports_count = 0
        tax_reports_count = 0

        profitloss_reports = self.env['custom.profitloss.report'].search([

            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date),
        ])

        taxes_reports = self.env['custom.tax.report'].search([
            ('create_date', '>=', start_date),
            ('create_date', '<=', end_date),
        ])

        for report in profitloss_reports:
            print(report.name)
            profitloss_reports_count += 1
        print(profitloss_reports_count)
        for report in taxes_reports:
            print(report.name)
            tax_reports_count += 1
        print(tax_reports_count)

        total_taxes=0
        invoices = self.env['account.move'].search([
            ('date', '>=', start_date),
            ('date', '<=', end_date),
            ('move_type', 'in', ['out_invoice', 'in_invoice'])
        ])
        for rec in invoices:
            total_taxes += rec.amount_tax
        print('total_taxes')
        print(total_taxes)

        # print(invoices.amount_untaxed)
        # print(invoices.amount_tax)
        # print(invoices.amount_total)

