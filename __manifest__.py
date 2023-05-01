{
    'name': 'Report on Gross Profit from Sales',
    'summary': 'Report on Gross Profit from Sales',
    'author': 'Mikola Ostroukh',
    'license': "LGPL-3",
    'category': 'Sale',
    'version': '15.0.1.0.0',
    'depends': ['sale','stock', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'report/report_sale_gross_profit_template.xml',
        'report/report_sale_gross_profit.xml',
        'wizard/gross_profit_report_wizard.xml',
        'views/gross_profit_sales_menu.xml',
    ],
}