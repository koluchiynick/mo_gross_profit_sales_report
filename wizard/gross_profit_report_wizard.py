from odoo import fields, models
from odoo.tools import date_utils
import datetime


class GrossProfitReport(models.TransientModel):
    _name = "gross.profit.sale.report.wizard"
    _description = "Sales Gross profit report"

    today = fields.Datetime.now()
    start_month = date_utils.start_of(
        today, "month")  #fields.Date.start_of(today, "month")

    date_from = fields.Date(string='Date From', default=start_month)
    date_to = fields.Date(string='Date to', default=today)
    company = fields.Many2one('res.company',
                              string='Company',
                              default=lambda self: self.env.user.company_id.id)
    partner_ids = fields.Many2many('res.partner', string='Partners')
    salesman_ids = fields.Many2many('res.users', string="Salesman")
    type_of_grouping = fields.Selection(
        [
            ("Partner/Product", "Partner/Product"),
            ("Salesman/Partner", "Salesman/Partner"),
            ("Salesman/Product", "Salesman/Product"),
            ("Salesman/Partner/Product", "Salesman/Partner/Product"),
        ],
        required=True,
        default="Partner/Product",
    )

    def generate_report_html(self):
        report_type = "qweb-html"
        return self._generate_report(report_type)

    def generate_report_pdf(self):
        report_type = "qweb-pdf"
        return self._generate_report(report_type)

    def _generate_report(self, report_type):
        data = {
            'form': self.read([])[0],
        }
        if report_type == "xlsx":
            report_name = "mo_gross_profit_sales_report.gross_profit_sale_xlsx"
        else:
            report_name = "mo_gross_profit_sales_report.gross_profit_sale"

        return self.env["ir.actions.report"].search(
            [("report_name", "=", report_name),
             ("report_type", "=", report_type)],
            limit=1,
        ).report_action(self, data=data)

    def generate_report_xlsx(self):
        report_type = "xlsx"
        return self._generate_report(report_type)
