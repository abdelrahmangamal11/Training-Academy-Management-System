from odoo import fields, models

class AcademyProductTemplate(models.Model):
    _inherit=["product.template"]

    course_id=fields.Many2one('academy.course', string='Course', readonly=True) 
  
    # _sql_constraints = [
    #     ('unique_course_product', 'UNIQUE(course_id)', 
    #      'A course can be linked to only one product.')
    # ]