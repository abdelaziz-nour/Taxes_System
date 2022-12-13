# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.misc import get_lang
from datetime import datetime


class final_accountant(models.Model):
    _name = 'final.accountant'
    _description = 'final accountant'

# same as account.tax.report.wizard but not transient
class Final_AccountCommonReport(models.Model):
    _name = "final.report"
    _description = "final report"

    final_create_date = fields.Datetime(string='Created on', default=datetime.now(), required=True, readonly=True,)
    final_accountant = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.uid, readonly=True,required=True )
    final_customer = fields.Many2one('res.partner', string='Customer',required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    journal_ids = fields.Many2many('account.journal', string='Journals', required=True, default=lambda self: self.env['account.journal'].search([('company_id', '=', self.company_id.id)]))
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('all', 'All Entries'),
                                    ], string='Target Moves', required=True, default='posted')


    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            self.journal_ids = self.env['account.journal'].search(
                [('company_id', '=', self.company_id.id)])
        else:
            self.journal_ids = self.env['account.journal'].search([])

    def _build_contexts(self, data):
        result = {}
        result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        result['strict_range'] = True if result['date_from'] else False
        result['company_id'] = data['form']['company_id'][0] or False
        result['final_customer'] = data['form']['final_customer'][0] or False
        result['final_accountant'] = data['form']['final_accountant'][0] or False
        result['final_create_date'] = data['form']['final_create_date'][0] or False
        return result

    def _print_report(self, data):
        raise NotImplementedError()

    def _print_report(self, data):
        return self.env.ref('accounting_pdf_reports.action_report_account_tax').report_action(self, data=data)

    def check_report(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['date_from', 'date_to', 'journal_ids', 'target_move', 'company_id', 'final_customer', 'final_accountant' , 'final_create_date'])[0]
        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context, lang=get_lang(self.env).code)
        print(data)
        # if (data['form']['final_customer']==(8, 'Custom Ink')):
        #     print('hi')
        #print(data['form']['final_customer'])
        return self.with_context(discard_logo_check=True)._print_report(data)




class ProfitLossReport(models.Model):
    _name = "profitloss.report"
    _inherit = "final.report"

    _rec_name = 'final_customer'

    @api.model
    def _get_account_report(self):
        reports = []
        if self._context.get('active_id'):
            menu = self.env['ir.ui.menu'].browse(self._context.get('active_id')).name
            reports = self.env['account.financial.report'].search([('name', 'ilike', menu)])
        return reports and reports[0] or False

    enable_filter = fields.Boolean(string='Enable Comparison')
    account_report_id = fields.Many2one('account.financial.report', string='Account Reports', required=True,
                                        default=_get_account_report)
    label_filter = fields.Char(string='Column Label',
                               help="This label will be displayed on report to show the balance computed for the given comparison filter.")
    filter_cmp = fields.Selection([('filter_no', 'No Filters'), ('filter_date', 'Date')], string='Filter by',
                                  required=True, default='filter_no')
    date_from_cmp = fields.Date(string='Date From')
    date_to_cmp = fields.Date(string='Date To')
    debit_credit = fields.Boolean(string='Display Debit/Credit Columns',
                                  help="This option allows you to get more details about the way your balances are computed. Because it is space consuming, we do not allow to use it while doing a comparison.")

    def _build_comparison_context(self, data):
        result = {}
        result['journal_ids'] = 'journal_ids' in data['form'] and data['form']['journal_ids'] or False
        result['state'] = 'target_move' in data['form'] and data['form']['target_move'] or ''
        if data['form']['filter_cmp'] == 'filter_date':
            result['date_from'] = data['form']['date_from_cmp']
            result['date_to'] = data['form']['date_to_cmp']
            result['strict_range'] = True
        return result

    def check_report(self):
        res = super(ProfitLossReport, self).check_report()
        data = {}
        data['form'] = \
        self.read(['account_report_id', 'date_from_cmp', 'date_to_cmp', 'journal_ids', 'filter_cmp', 'target_move'])[0]
        for field in ['account_report_id']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        comparison_context = self._build_comparison_context(data)
        res['data']['form']['comparison_context'] = comparison_context
        return res

    def _print_report(self, data):
        data['form'].update(self.read(
            ['date_from_cmp', 'debit_credit', 'date_to_cmp', 'filter_cmp', 'account_report_id', 'enable_filter',
             'label_filter', 'target_move'])[0])
        return self.env.ref('accounting_pdf_reports.action_report_financial').report_action(self, data=data,
                                                                                            config=False)






