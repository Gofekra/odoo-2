{
    'name' : 'OpenERP or Odoo Pet Store',
    'version': '1.0',
    'summary': 'Sell pet toys',
    'category': 'Tools',
    'description':"""""",

    'data': [
        "views/petstore.xml",
        "data/petstore_data.xml",
        "security/oepetstore.message_of_the_day.csv",
    ],
    'depends' : ['sale_stock'],

    'qweb':
        ['static/src/xml/*.xml'],

    'application': True,
}
