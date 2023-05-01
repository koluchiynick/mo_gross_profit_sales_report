from odoo import models, _
from odoo.exceptions import UserError

import datetime


class ReportSaleGrossProfit(models.AbstractModel):
    _name = 'report.mo_gross_profit_sales_report.gross_profit_sale'
    _description = 'Report on Gross Profit from Sales'

    def _data_so_groupby(self,
                         sale_orders_line,
                         name_grouping='order_partner_id',
                         name_subgrouping='product_id',
                         name_sub2_grouping=''):
        data_groupby = {}
        for so_id in sale_orders_line:
            grouping_id = so_id[name_grouping]
            subgrouping_id = so_id[name_subgrouping]
            qty_delivered = so_id.qty_delivered
            price_subtotal = so_id.price_subtotal
            purchase_price = so_id.purchase_price
            margin = so_id.margin
            margin_percent = margin / price_subtotal * 100
            cost = purchase_price * qty_delivered

            if not data_groupby.get(grouping_id):
                data_groupby.update({
                    grouping_id: {
                        'qty_delivered': qty_delivered,
                        'price_subtotal': price_subtotal,
                        'cost': cost,
                        'margin': margin,
                        'margin_percent': margin_percent,
                        'len_subgrouping': 0,
                        'subgrouping': {},
                    }
                })
                grouping = data_groupby[grouping_id]
            else:
                grouping = data_groupby[grouping_id]
                grouping['qty_delivered'] += qty_delivered
                grouping['price_subtotal'] += price_subtotal
                grouping['cost'] += cost
                grouping['margin'] += margin
                grouping['margin_percent'] = (grouping['margin'] /
                                              grouping['price_subtotal'] * 100)

            if not grouping['subgrouping'].get(subgrouping_id):
                grouping['subgrouping'].update({
                    subgrouping_id: {
                        'qty_delivered': qty_delivered,
                        'price_subtotal': price_subtotal,
                        'cost': cost,
                        'margin': margin,
                        'margin_percent': margin_percent,
                        'len_subgrouping': 0,
                        'sub2_grouping': {},
                    }
                })
                grouping['len_subgrouping'] += 1
                subgrouping = grouping['subgrouping'][subgrouping_id]
            else:
                subgrouping = grouping['subgrouping'][subgrouping_id]
                subgrouping['qty_delivered'] += qty_delivered
                subgrouping['price_subtotal'] += price_subtotal
                subgrouping['cost'] += cost
                subgrouping['margin'] += margin
                subgrouping['margin_percent'] = (
                    subgrouping['margin'] / subgrouping['price_subtotal'] *
                    100)

            if not name_sub2_grouping == '':
                sub2_grouping_id = so_id[name_sub2_grouping]
                if not subgrouping['sub2_grouping'].get(sub2_grouping_id):
                    subgrouping['sub2_grouping'].update({
                        sub2_grouping_id: {
                            'qty_delivered': qty_delivered,
                            'price_subtotal': price_subtotal,
                            'cost': cost,
                            'margin': margin,
                            'margin_percent': margin_percent,
                        }
                    })
                    grouping['len_subgrouping'] += 1
                    subgrouping['len_subgrouping'] += 1
                else:
                    sub2_grouping = subgrouping['sub2_grouping'][
                        sub2_grouping_id]
                    sub2_grouping['qty_delivered'] += qty_delivered
                    sub2_grouping['price_subtotal'] += price_subtotal
                    sub2_grouping['cost'] += cost
                    sub2_grouping['margin'] += margin
                    sub2_grouping['margin_percent'] = margin_percent

        return data_groupby

    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))

        form_data = data['form']
        wizard_id = form_data['id']
        date_from = form_data['date_from']
        date_to = form_data['date_to']
        company = form_data['company']
        partner_ids = form_data['partner_ids']
        salesman_ids = form_data['salesman_ids']
        type_of_grouping = form_data['type_of_grouping']

        domain_line = [('order_id.date_order', '>=', date_from),
                       ('order_id.date_order', '<=', date_to),
                       ('state', '=', 'sale'), ('company_id', '=', company[0]),
                       ('qty_delivered', '>', 0)]
        if partner_ids:
            domain_line += [('order_partner_id', 'in', partner_ids)]
        if salesman_ids:
            domain_line += [('salesman_id', 'in', salesman_ids)]

        sale_orders_line = self.env['sale.order.line'].search(domain_line)

        data_report = {}
        three_groupings = False
        colspan = 2
        if type_of_grouping == 'Salesman/Partner':
            data_report = self._data_so_groupby(sale_orders_line,
                                                'salesman_id',
                                                'order_partner_id')
        elif type_of_grouping == 'Salesman/Product':
            data_report = self._data_so_groupby(sale_orders_line,
                                                'salesman_id', 'product_id')
        elif type_of_grouping == 'Salesman/Partner/Product':
            data_report = self._data_so_groupby(sale_orders_line,
                                                'salesman_id',
                                                'order_partner_id',
                                                'product_id')
            three_groupings = True
            colspan = 3
        else:
            data_report = self._data_so_groupby(sale_orders_line,
                                                'order_partner_id',
                                                'product_id')

        return {
            'data': form_data,
            "docs":
            self.env["gross.profit.sale.report.wizard"].browse(wizard_id),
            'data_report': data_report,
            'type_of_grouping': type_of_grouping,
            'three_groupings': three_groupings,
            'colspan': colspan,
            'report_date': datetime.datetime.now().strftime("%Y-%m-%d"),
        }
