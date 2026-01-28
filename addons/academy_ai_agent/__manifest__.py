{
    'name': 'Academy AI Agent',
    'version': '1.0',
    'description': 'Allows users to create courses, enrollments, etc., via chat commands parsed by AI safely.',
    'category': 'Education',
    'author': 'Abdelrahman Mohamed',
    'depends': ['academy', 'mail', 'base'],
    'data': [
    'views/chat_command_views.xml',
    'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
}
