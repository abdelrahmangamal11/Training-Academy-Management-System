from datetime import datetime
from odoo import api, models

class StudentTranscriptParser(models.AbstractModel):
    _name = "report.academy.report_student_transcript_template"

    @api.model
    def _get_report_values(self, docids, data=None):
        partners = self.env['res.partner'].browse(docids)


        partner_data = []
        for partner in partners:
            enrollments = self.env['academy.enrollment'].search([
                ('student_id', '=', partner.id)
            ])

            total_courses = len(enrollments)
            total_grade = sum(enrollments.mapped('grade'))
            avg_grade = total_grade / total_courses if total_courses else 0

            # Get top 3 courses by grade
            course_list = []
            for enrollment in enrollments:
                course_list.append({
                    'course_name': enrollment.course_id.name,
                    'grade': enrollment.grade,
                })

            top_courses=sorted(course_list, key=lambda c: c['grade'], reverse=True)[:3]

            partner_data.append({
                'partner': partner,
                'total_courses': total_courses,
                'average_grade': avg_grade,
                'enrollments': enrollments,
                'top_courses': top_courses,
            })
    
        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'docs': partners,
            'report_date': datetime.now(),
            'partner_data': partner_data,
            'company': self.env.company,
        }
