from odoo import models, fields , api

class CustomSale(models.Model):
    _inherit =["sale.order"]

    course_id=fields.Many2one('academy.course', string='Course')

    def action_confirm(self):
        res=super(CustomSale,self).action_confirm()
        for order in self:
            for line in order.order_line:
                if line.product_id.course_id:
                    self.env['academy.enrollment'].create({
                        'student_id':self.partner_id.id,
                        'course_id':line.product_id.course_id.id,
                        'state':'draft'
                    })
        return res
   