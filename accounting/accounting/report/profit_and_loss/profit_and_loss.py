# Copyright (c) 2013, Rutwik and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe import _
from frappe.utils import flt

from accounting.accounting.report.financial_statements import get_data, get_columns

def execute(filters=None):
    columns, data = [], []
    income = get_data('Income', 'Debit', filters.from_date, filters.to_date)
    expense = get_data('Expense', 'Debit', filters.from_date, filters.to_date)

    data.extend(income or [])
    data.extend(expense or [])
    print('Data: ', data)

    net_profit_loss = get_net_profit_loss(income, expense)

    if net_profit_loss:
        data.append(net_profit_loss)

    columns = get_columns()
    chart = get_chart_data(columns, income, expense, net_profit_loss)

    report_summary = get_report_summary(income, expense, net_profit_loss)

    return columns, data, None, chart, report_summary

def get_net_profit_loss(income, expense):
    total = 0
    net_profit_loss = {
        "account_name": "'" + _("Profit for the year") + "'",
        "account": "'" + _("Profit for the year") + "'",
        "warn_if_negative": True,
    }

    total_income = flt(income[-2]['opening_balance'], 3) if income else 0
    total_expense = flt(expense[-2]['opening_balance'], 3) if expense else 0

    net_profit_loss['opening_balance'] = total_income - total_expense
    print(total_income, total_expense)

    return net_profit_loss

def get_report_summary(income, expense, net_profit_loss):
    net_income, net_expense, net_profit = 0.0, 0.0, 0.0

    net_income = flt(income[-2]['opening_balance'], 3)
    net_expense = flt(expense[-2]['opening_balance'], 3)
    net_profit = flt(net_profit_loss['opening_balance'], 3)

    profit_label = _('Net Profit')
    income_label = _('Total Income')
    expense_label = _('Total Expense')

    return [
        {
            'value': net_income,
            'label': income_label,
            'datatype': 'Currency'
        },
        { 'type': 'separator', 'value': '-' },
        {
            'value': net_expense,
            'label': expense_label,
            'datatype': 'Currency'
        },
        { 'type': 'separator', 'value': '=', 'color': 'blue' },
        {
            'value': net_profit,
            'indicator': 'Green' if net_profit > 0 else 'Red',
            'label': profit_label,
            'datatype': 'Currency'
        }
    ]

def get_chart_data(columns, income, expense, net_profit_loss):
    labels = [d.get("label") for d in columns[2:]]

    income_data, expense_data, net_profit = [], [], []

    for p in columns[2:]:
        if income:
            income_data.append(income[-2].get(p.get("fieldname")))
        if expense:
            expense_data.append(expense[-2].get(p.get("fieldname")))
        if net_profit_loss:
            net_profit.append(net_profit_loss.get(p.get("fieldname")))

    datasets = []
    if income_data:
        datasets.append({'name': _('Income'), 'values': income_data})
    if expense_data:
        datasets.append({'name': _('Expense'), 'values': expense_data})
    if net_profit:
        datasets.append({'name': _('Net Profit/Loss'), 'values': net_profit})

    chart = {
        "data": {
            'labels': labels,
            'datasets': datasets
        }
    }

    chart["type"] = "bar"
    chart["fieldtype"] = "Currency"

    return chart
