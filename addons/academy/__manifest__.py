{
    'name': "Academy Lab Module",
    'version': '1.0',
    'author': "Abdelrahman Mohamed",
    'category': 'Category',
    'description': "",
    'depends':['base','mail','contacts','sale','account'],
    'data': [
        'security/academy_security.xml',
        'security/ir.model.access.csv',
        'wizard/product_wizard_view.xml',   
        'views/course_views.xml',
        'views/category_views.xml',
        'views/enrollment_views.xml',
        'views/partner_views.xml',
        'views/product_template_views.xml',
        'views/menus.xml',
        'report/certificate_report.xml',
        "report/course_enrollment.xml",
        'wizard/enrollment_report_wizard_view.xml',
        "report/enrollment_report_date.xml",
        "report/student_transcript_report.xml"
        
    ],
    'application': True,
}