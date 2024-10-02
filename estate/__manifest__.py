{
    'name': 'Real Estate',
    'sequence' : 1,
    'author': 'Asmaa AZ',
    'data' : ['security/ir.model.access.csv',
              'views/estate_property_views.xml',
              'views/estate_property_type_views.xml',
              'views/estate_property_tag_views.xml',
              'views/estate_property_offer.xml',
              'views/res_users_view.xml',
              'views/estate_menus.xml',
              'report/real_estate_property_report.xml',
              'report/property_users_report.xml',
              ],
    'depends':['base'],
    'application': True,
}