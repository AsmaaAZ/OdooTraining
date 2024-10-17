{
    'name': 'Library Management',
    'sequence' : 3,
    'author': 'Asmaa AZ',
    'data' : ['security/ir.model.access.csv',
              'views/library_book_view.xml',
              'views/library_author_view.xml',
              'views/library_menus.xml',
              'report/library_book_report.xml',
              ],
    'depends':['base'],
    'application': True,
}