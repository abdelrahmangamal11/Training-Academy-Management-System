from odoo import models, fields, api

class Session(models.Model):
    _name="academy.session"
    _description=''
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name='code'

    no=fields.Integer()
    code=fields.Char()
    description=fields.Text()
    active=fields.Boolean(default=True)