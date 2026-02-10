from odoo import models, fields, api


class CourseHistory(models.Model):  
    _name="academy.course.history"
    
    ## Fields ##
    user_id=fields.Many2one('res.users', string='User')
    course_id=fields.Many2one('academy.course', string='Course')
    old_state=fields.Char(string='Old State')
    new_state=fields.Char(string='New State')