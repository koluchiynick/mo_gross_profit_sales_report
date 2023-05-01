from odoo import models, _


class ReportSaleGrossProfitXLSX(models.AbstractModel):
    _name = 'report.mo_gross_profit_sales_report.gross_profit_sale_xlsx'
    _description = 'Report on Gross Profit from Sales XLSX'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):

        res_data = self.env[
            'report.mo_gross_profit_sales_report.gross_profit_sale']._get_report_values(
                None, data)
        data_report = res_data['data_report']
        colspan = res_data['colspan']

        sheet = workbook.add_worksheet(str('report'))
        merge_format = workbook.add_format({
            'font_size': 14,
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        bold = workbook.add_format({
            'bold': True,
            'font_size': 14,
        })
        format_company = workbook.add_format({
            'font_size': 14,
        })
        sheet.merge_range('A1:H1', '', merge_format)
        sheet.write('A1', 'Report on Gross Profit from Sales', merge_format)
        sheet.merge_range('A2:H2', '', merge_format)
        sheet.write_rich_string('A2', 'Company:', format_company,
                                res_data['data']['company'][1], merge_format)
        sheet.merge_range('A3:H3', '', merge_format)
        sheet.write_rich_string('A3', 'For the period from ', bold,
                                res_data['data']['date_from'], bold, ' to ',
                                bold, res_data['data']['date_to'],
                                merge_format)

        format_tab = workbook.add_format({
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'border': 1,
        })
        format_tab.set_text_wrap()
        sheet.write(5, 0, 'No', format_tab)
        sheet.merge_range(5, 1, 5, colspan, res_data['type_of_grouping'],
                          format_tab)
        sheet.write(5, colspan + 1, 'Quantity', format_tab)
        sheet.write(5, colspan + 2, 'Amount of Sales', format_tab)
        sheet.write(5, colspan + 3, 'Cost', format_tab)
        sheet.write(5, colspan + 4, 'Margin', format_tab)
        sheet.write(5, colspan + 5, 'Margin %', format_tab)

        format_grouping = workbook.add_format({
            'font_size': 10,
            'align': 'left',
            'border': 1,
        })
        format_grouping.set_text_wrap()
        format_number_grouping = workbook.add_format({
            'font_size': 10,
            'align': 'right',
            'num_format': '0',
            'border': 1,
        })
        format_float_grouping = workbook.add_format({
            'font_size': 10,
            'align': 'right',
            'num_format': '0.00',
            'border': 1,
        })
        format_grouping.set_bg_color('gray')
        format_number_grouping.set_bg_color('gray')
        format_float_grouping.set_bg_color('gray')

        format_subgrouping = workbook.add_format({
            'font_size': 10,
            'align': 'left',
            'border': 1,
        })
        format_subgrouping.set_text_wrap()
        format_number_subgrouping = workbook.add_format({
            'font_size': 10,
            'align': 'right',
            'num_format': '0',
            'border': 1,
        })
        format_float_subgrouping = workbook.add_format({
            'font_size': 10,
            'align': 'right',
            'num_format': '0.00',
            'border': 1,
        })

        sheet.set_column(0, 1, 4)
        sheet.set_column(2, 2, 60)
        sheet.set_column(3, 8, 12)
        if colspan > 2:
            format_subgrouping.set_bg_color('orange')
            format_number_subgrouping.set_bg_color('orange')
            format_float_subgrouping.set_bg_color('orange')
            sheet.set_column(2, 2, 4)
            sheet.set_column(3, 3, 60)

        format_sub2_grouping = workbook.add_format({
            'font_size': 10,
            'align': 'left',
            'border': 1,
        })
        format_sub2_grouping.set_text_wrap()
        format_number_sub2_grouping = workbook.add_format({
            'font_size': 10,
            'align': 'right',
            'num_format': '0',
            'border': 1,
        })
        format_float_sub2_grouping = workbook.add_format({
            'font_size': 10,
            'align': 'right',
            'num_format': '0.00',
            'border': 1,
        })

        if data_report:
            row = 6
            num_str = 1
            for grouping_id in data_report:
                grouping = data_report[grouping_id]
                sheet.write(row, 0, num_str, format_number_grouping)
                sheet.merge_range(row, 1, row, colspan, grouping_id.name,
                                  format_grouping)
                sheet.write_number(row, colspan + 1, grouping['qty_delivered'],
                                   format_float_grouping)
                sheet.write_number(row, colspan + 2,
                                   grouping['price_subtotal'],
                                   format_float_grouping)
                sheet.write_number(row, colspan + 3, grouping['cost'],
                                   format_float_grouping)
                sheet.write_number(row, colspan + 4, grouping['margin'],
                                   format_float_grouping)
                sheet.write_number(row, colspan + 5,
                                   grouping['margin_percent'],
                                   format_float_grouping)
                row += 1
                num_str += 1
                if grouping['subgrouping']:
                    sub_num_str = 1
                    for subgrouping_id in grouping['subgrouping']:
                        subgrouping = grouping['subgrouping'][subgrouping_id]
                        sheet.write(row, 1, sub_num_str,
                                    format_number_subgrouping)
                        if colspan > 2:
                            sheet.merge_range(row, 2, row, colspan,
                                              subgrouping_id.display_name,
                                              format_subgrouping)
                        else:
                            sheet.write(row, 2, subgrouping_id.display_name,
                                        format_subgrouping)
                        sheet.write_number(row, colspan + 1,
                                           subgrouping['qty_delivered'],
                                           format_float_subgrouping)
                        sheet.write_number(row, colspan + 2,
                                           subgrouping['price_subtotal'],
                                           format_float_subgrouping)
                        sheet.write_number(row, colspan + 3,
                                           subgrouping['cost'],
                                           format_float_subgrouping)
                        sheet.write_number(row, colspan + 4,
                                           subgrouping['margin'],
                                           format_float_subgrouping)
                        sheet.write_number(row, colspan + 5,
                                           subgrouping['margin_percent'],
                                           format_float_subgrouping)
                        sheet.set_row(row, None, None, {'level': 1})
                        row += 1
                        sub_num_str += 1
                        if subgrouping['sub2_grouping']:
                            sub2_num_str = 1
                            for sub2_grouping_id in subgrouping[
                                    'sub2_grouping']:
                                sub2_grouping = subgrouping['sub2_grouping'][
                                    sub2_grouping_id]
                                sheet.write(row, 2, sub2_num_str,
                                            format_number_sub2_grouping)
                                sheet.write(row, 3,
                                            sub2_grouping_id.display_name,
                                            format_sub2_grouping)
                                sheet.write_number(
                                    row, 4, sub2_grouping['qty_delivered'],
                                    format_float_sub2_grouping)
                                sheet.write_number(
                                    row, 5, sub2_grouping['price_subtotal'],
                                    format_float_sub2_grouping)
                                sheet.write_number(row, 6,
                                                   sub2_grouping['cost'],
                                                   format_float_sub2_grouping)
                                sheet.write_number(row, 7,
                                                   sub2_grouping['margin'],
                                                   format_float_sub2_grouping)
                                sheet.write_number(
                                    row, 8, sub2_grouping['margin_percent'],
                                    format_float_sub2_grouping)
                                sheet.set_row(row, None, None, {'level': 2})
                                row += 1
                                sub2_num_str += 1
