# -*- coding: utf-8 -*-

{
    'name': 'change_tree_view',
    'version': '1.0',
    'author': 'Ltd',
    'summary': 'Web tool',
    'description' : """
         Odoo tree view  :
        This module allows you to change any tree view to meet your requirement from interface not coding, Also you can sort the columns as per your requirement, by using this feature, you can print and export any report which you want.
        ==============================================================
        
        * More features: -
        1- Change tree columns from interface as administrator.
        2- You can sort columns from Odoo interface (Drag & Drop)
        3- After customize tree view, you can print it as PDF or Excel.
        4- Every user can customize his tree view as per his requirement.
        5- Security: - * Admin can give custom tree privilege for specific users to customize his tree view. * The users can select and show the fields ONLY which they have privilege to see it.
          
          
          
        By using this module you can changes the fields of the current view by adding or removing fields from the tree using the jlist.
        * Also you can using this module for reporting.
    """,
    'website': '',
    'category': 'web',
    'sequence': 17,
    'data': [
             'security/tree_security.xml',
             'security/ir.model.access.csv',
             'wizard/change_tree_view_wizard_view.xml',
             'views/customize_tree.xml'
    ],
    'images': ['images/1.png','images/2.png','images/3.png','images/4.png','images/5.png','images/6.png'],
    'qweb' : ['static/src/xml/*.xml'],
    'auto_install': False,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
