# -*- coding: utf-8 -*-
{
    'name': "Kursus",

    'summary': "Aplikasi Kursus",

    'description': """
Long description of module's purpose
    """,

    'author': "Cendana 2000",
    'website': "https://www.cendana2000.com",
    'application': True,


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '18.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'product', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',

        'security/groups.xml',
        'security/ir.model.access.csv',
        'wizards/kursus_wizard.xml',

        'data/ir_sequence_data.xml',

        'views/menu_kursus.xml',
        'views/kursus.xml',
        'views/instruktur.xml',
        'views/provinsi.xml',
        'views/kota.xml',
        'views/kecamatan.xml',
        'views/desa.xml',
        'views/peserta.xml',
        'views/sesi_kursus.xml',
        'views/product_inherit.xml',
        'views/pendaftaran.xml',
        'views/daftar_hadir.xml',



        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],


    # custom assets
    #  "assets": {
    #     "web.assets_backend": [
    #         "custom_text_widget/static/src/js/text_transform_widget.js",
    #     ],
    # },
}

