from odoo import fields, models

class EnrollmentWizard(models.TransientModel):
    _name = 'academy.enrollment.wizard.report'
    _description = 'Enrollment Wizard'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    student_id = fields.Many2one('res.partner', string='Student')
   

    def action_generate_report(self):
        domain = []
        if self.start_date:
            domain += [('enrollment_date', '>=', self.start_date)]
        if self.end_date:
            domain += [('enrollment_date', '<=', self.end_date)]
        if self.student_id:
            domain += [('student_id', '=', self.student_id.id)]

        print("Domain:", domain)
        enrollments = self.env['academy.enrollment'].search_read(domain)
        print("Enrollments Found:", enrollments)

        data={
            'enrollments':enrollments
        }
        return self.env.ref('academy.report_enrollment_date').report_action(self, data=data)
    






    #    # enrollments = self.env['academy.enrollment'].search([
        #     ('enrollment_date', '>=', self.start_date),
        #     ('enrollment_date', '<=', self.end_date),
        #     ('student_id', '=', self.student_id.id) if self.student_id else ('id', '!=', False)
        # ])