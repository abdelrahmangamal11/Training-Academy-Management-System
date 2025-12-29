from odoo import models, fields


class AccountMove(models.Model):
    _inherit = ['account.move']

    enrollment_ids=fields.One2many('academy.enrollment', 'invoice_id', string='Enrollments')
    
    def action_post(self):
        res=super(AccountMove,self).action_post()
        for move in self:
            for line in move.invoice_line_ids:
                if line.product_id.course_id:
                    enrollment=self.env['academy.enrollment'].search([
                        ('student_id', '=', move.partner_id.id),
                        ('course_id', '=', line.product_id.course_id.id)   
                    ],limit=1)
                   
                    if enrollment:
                        enrollment.write({
                        'state':'confirmed',
                        'invoice_id': self.id
                        })
        return res
