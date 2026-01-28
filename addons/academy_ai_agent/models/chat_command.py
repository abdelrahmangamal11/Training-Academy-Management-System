from odoo import models, fields, api
from .academy_course_ai import AIParserService

class AcademyChatCommand(models.Model):
    _name = 'academy.chat.command'
    _description = 'AI Chat Agent'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    session_id = fields.Many2one('academy.chat.session', string='Session', ondelete='cascade')
    
    message = fields.Text(string="User Message", required=True, tracking=True)
    response = fields.Text(string="AI Response", readonly=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('processing', 'Processing'),  
        ('done', 'Done'),
        ('failed', 'Failed')
    ], default='draft', tracking=True)

    def process_command(self):
        self.ensure_one()
        
        self.state = 'processing'
        
        service = AIParserService()
        try:
            data = service.parse(self.message)


            if data.get('action') == 'chat':
                self.response = data.get('message')
                self.state = 'done'

            elif data.get('action') == 'get_accounting_report':
            
                income_domain = [('account_id.account_type', 'in', ['income', 'income_other']), ('parent_state', '=', 'posted')]
                expense_domain = [('account_id.account_type', 'in', ['expense', 'expense_depreciation', 'expense_direct_cost']), ('parent_state', '=', 'posted')]
            
                incomes = sum(self.env['account.move.line'].search(income_domain).mapped('credit')) - sum(self.env['account.move.line'].search(income_domain).mapped('debit'))
                expenses = sum(self.env['account.move.line'].search(expense_domain).mapped('debit')) - sum(self.env['account.move.line'].search(expense_domain).mapped('credit'))
            
                net_profit = incomes - expenses
                status = "losing" if net_profit >= 0 else "earning"

                self.response = (
                    f"incomes{incomes}\n"
                    f"إجمالي المصروفات: {expenses}\n"
                    f"{abs(net_profit)}"
                )
                self.state = 'done'

            elif data.get('action') == 'create_course':
                vals = {
                    'name': data.get('name'),
                    'code': data.get('code'),
                    'max_students': data.get('max_students', 20),
                }
                if data.get('start_date'):
                    vals['start_date'] = data.get('start_date')
                if data.get('end_date'):
                    vals['end_date'] = data.get('end_date')

                course = self.env['academy.course'].create(vals)
                self.response = data.get('success_msg')
                self.state = 'done'

            else:
                self.response = data.get('message')
                self.state = 'failed'

            self.message_post(body=f"<b>Gemy:</b> {self.response}")
            
            # إضافة هذا السطر للـ reload
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }

        except Exception as e:
            self.state = 'failed'
            self.response = f"عذراً، حدث خطأ: {str(e)}"
            
    # class AcademyChatSession(models.Model):
    #     _name = 'academy.chat.session'
    #     _description = 'AI Session'
    #     _order = 'create_date desc'

    #     name = fields.Char(string='Session', compute='_compute_name', store=True)
    #     command_ids = fields.One2many('academy.chat.command', 'session_id', string='Messages')
    #     state = fields.Selection([('active', 'Active'), ('closed', 'Closed')], default='active')

    #     @api.depends('command_ids')
    #     def _compute_name(self):
    #         for rec in self:
    #             rec.name = rec.command_ids[0].message[:30] if rec.command_ids else "New Chat"

    #     def action_send_message(self):
    #         return {
    #             'name': 'Ask Gemy',
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'academy.chat.command',
    #             'view_mode': 'form',
    #             'view_id': self.env.ref('academy.view_chat_command_quick_form').id, # تأكد من اسم الموديول هنا
    #             'target': 'new',
    #             'context': {'default_session_id': self.id},
    #         }
            
        # self.ensure_one()
        # service = AIParserService()
        # try:
        #     data = service.parse(self.message)

        #     vals = {
        #         'name': data.get('name'),
        #         'code': data.get('code'),
        #         'max_students': data.get('max_students', 20),
        #         }

        #     if data.get('start_date'):
        #         vals['start_date'] = data.get('start_date')
            
        #     if data.get('end_date'):
        #         vals['end_date'] = data.get('end_date')

        #     course = self.env['academy.course'].create(vals)

        #     self.response = f"the course created succesfully {course.name}"
        #     self.state = 'done'

        #     self.message_post(body=self.response)
        #     self.message_post(body=f"<b>Gemy:</b> {self.response}")
        # except Exception as e:
        #     self.state = 'failed'
        #     self.response = str(e)

         