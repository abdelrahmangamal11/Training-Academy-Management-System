from odoo import models,fields,api

class Partner(models.Model):  
    _inherit = 'res.partner'

    is_student = fields.Boolean(string='Student')
    is_instructor = fields.Boolean(string='Instructor')
    student_enrollment_ids=fields.One2many('academy.enrollment', 'student_id', string='Student Enrollments')
    instructor_course_ids=fields.One2many('academy.course', 'instructor_id', string='Instructor Courses')
    total_courses_enrolled = fields.Integer(compute='_compute_total_courses_enrolled')
    total_courses_teaching = fields.Integer(compute='_compute_total_courses_teaching')

    def action_do_something(self):
        print("do something ")

    @api.depends('student_enrollment_ids')
    def _compute_total_courses_enrolled(self):
        for partner in self:
            partner.total_courses_enrolled = len(partner.student_enrollment_ids)                                      

    @api.depends('instructor_course_ids')
    def _compute_total_courses_teaching(self):
        for partner in self:
            partner.total_courses_teaching = len(partner.instructor_course_ids) 

    def action_view_student_enrollments(self):
        return {
            'name': 'Student Enrollments',
            'type': 'ir.actions.act_window',
            'res_model': 'academy.enrollment',
            'view_mode': 'tree,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id}
        }
    
    def action_view_instructor_courses(self):
        return {
            'name': 'Teaching Courses',
            'type': 'ir.actions.act_window',
            'res_model': 'academy.course',
            'view_mode': 'list,form',
            'domain': [('instructor_id', '=', self.id)],
            'context': {'default_instructor_id': self.id}
        }