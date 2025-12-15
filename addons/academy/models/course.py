from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Course(models.Model):  
    _name="academy.course"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    ## Fields ##
    name = fields.Char(string='Course Name', required=True, tracking=True)
    code= fields.Char(string='Course Code', required=True, index=True)
    description = fields.Text(string='Course Description', tracking=True)
    instructor_id=fields.Many2one('res.partner')
    category_id=fields.Many2one('academy.course.category', string='Category')   
    duration_hours=fields.Float(string='Duration (Hours)')
    max_students=fields.Integer(string='Maximum Students', default=20)
    state=fields.Selection([("draft","Draft"),
                            ("published","Published"),
                            ('in_progress','In_progress'),
                            ('done','Done'),
                            ('cancelled','Cancelled')],default="draft",tracking=True)
    start_date=fields.Date(string='Start Date', tracking=True)
    end_date=fields.Date(string='End Date', tracking=True)
    enrollment_ids=fields.One2many("academy.enrollment","course_id",string="Enrollments")
    enrolled_count=fields.Integer(string='Number of Enrolled Students', compute='_compute_enrolled_count', store=True)
    available_seats=fields.Integer(string='Available Seats', compute='_compute_available_seats', store=True)
    is_full = fields.Boolean(string='Is Full', compute='_compute_is_full', store=True)
    instructor_name=fields.Char(string='Instructor Name', related='instructor_id.name', store=True)

    ## Constraints ##
    _sql_constraints=[('unique_course-code','unique(code)','code must be unique')]

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for course in self:
            if  course.end_date < course.start_date:
                raise ValidationError('End Date cannot be earlier than Start Date.')        

    @api.constrains('max_students')
    def _check_max_students(self):
        for course in self:
            if course.max_students <= 0:
                raise ValidationError('Maximum Students must be greater than zero.')

    ## Computation Methods ##

    @api.onchange('code')
    def _onchange_code_upper(self):
        if self.code:
            self.code = self.code.upper()

    @api.depends('enrollment_ids')
    def _compute_enrolled_count(self):
        for course in self:
            course.enrolled_count = len(course.enrollment_ids.filtered(lambda e: e.state == 'confirmed'))

    @api.depends('max_students', 'enrolled_count')
    def _compute_available_seats(self):
        for course in self:
            course.available_seats =max(course.max_students - course.enrolled_count, 0)       
    
    @api.depends('available_seats')
    def _compute_is_full(self):
        for course in self:
            course.is_full = course.available_seats <= 0

    ## Action Methods ##
    def action_publish(self):
        for rec in self:
            rec.state = 'published'
    
    def action_start(self):
        for rec in self:
            rec.state = 'in_progress'   
    
    def action_complete(self):      
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancelled' 
    
    def action_set_draft(self):
        for rec in self:
            rec.state = 'draft' 
    
    def action_view_enrollments(self):
        return {
            'name': 'Enrollments',
            'type': 'ir.actions.act_window',
            'res_model': 'academy.enrollment',
            'view_mode': 'list,form',
            'domain': [('course_id', '=', self.id)],
            'context': {
                'default_course_id': self.id,
                'create': True,
            }
        }
    
            
    