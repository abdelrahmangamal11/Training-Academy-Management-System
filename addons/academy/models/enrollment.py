from odoo import models,fields,api 
from odoo.exceptions import ValidationError

class Enrollment(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _name="academy.enrollment"

    ## Fields ##
    student_id = fields.Many2one(  'res.partner',string='Student',required=True)
    course_id = fields.Many2one( 'academy.course', string='Course',required=True)
    enrollment_date = fields.Date(string='Enrollment Date')
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
            ('completed', 'Completed')
        ], string='Status',default='draft',tracking=True)
    grade = fields.Float(string='Grade')
    attendance_percentage = fields.Float(string='Attendance Percentage')
    notes = fields.Text(string='Notes')
    user_id = fields.Many2one(
        "res.users",
        string="User",
        related="student_id.user_id",
        store=True,
        readonly=True,
    )

    ## Computed Fields ##
    student_name=fields.Char(string='Student Name', related='student_id.name', store=True)
    course_name=fields.Char(string='Course Name', related='course_id.name', store=True)
    passed = fields.Boolean(string='Passed', compute='_compute_passed', store=True)

 

    ## Computation Methods ##
    def _compute_passed(self):
        passing_grade = 60.0
        passing_attendance=75.0  
        for enrollment in self:
            enrollment.passed = enrollment.grade >= passing_grade and enrollment.attendance_percentage >= passing_attendance

    ## Constraints ##
    _sql_constraints = [(
        'unique_enrollment',
        'unique(student_id, course_id)',
        'A student can enroll only once in the same course.'
    )]

    @api.constrains('state')
    def _check_available_seats(self):
        for rec in self:
            if rec.state == 'confirmed' and rec.course_id.available_seats <= 0:
                raise ValidationError('Cannot confirm enrollment. Course is full.')


    ## Action Methods ##
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'   

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_complete(self):
        for rec in self:
            rec.state = 'completed' 