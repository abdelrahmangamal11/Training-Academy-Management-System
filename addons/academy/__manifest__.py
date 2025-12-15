{
    'name': "Academy Lab Module",
    'version': '1.0',
    'author': "Abdelrahman Mohamed",
    'category': 'Category',
    'description': "",
    'depends':['base','mail','contacts'],
    'data': [
        'security/academy_security.xml',
        'security/ir.model.access.csv',
        'views/course_views.xml',
        'views/category_views.xml',
        'views/enrollment_views.xml',
        'views/partner_views.xml',
        'views/menus.xml',
    ],
    'application': True,
}