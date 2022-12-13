# -*- coding: utf-8 -*-

from odoo import models, fields, api


class my_admin(models.Model):
    _name = 'final.admin'
    _description = 'final admin'

class ResPartner(models.Model):
    _inherit = 'res.partner'

class adminTaxes(models.Model):
    _inherit = 'account.tax'
