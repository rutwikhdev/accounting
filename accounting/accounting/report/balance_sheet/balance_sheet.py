# Copyright (c) 2013, Rutwik and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from accounting.accounting.report.financial_statements import get_data, get_columns
from frappe import _

def execute(filters=None):
    data = []
    asset = get_data('Asset', 'Debit', filters.from_date, filters.to_date)
    liability = get_data('Liability', 'Debit', filters.from_date, filters.to_date)
    equity = get_data('Equity', 'Credit', filters.from_date, filters.to_date)

    data.extend(asset or [])
    data.extend(liability or [])
    data.extend(equity or [])

    columns = get_columns()
    chart = get_chart_data(columns, asset, liability, equity)
    return columns, data, None, chart, None

def get_chart_data(columns, asset, liability, equity):
    labels = [d.get("label") for d in columns[2:]]

    asset_data, liability_data, equity_data = [], [], []

    for p in columns[1:]:
        if asset:
            asset_data.append(asset[-2].get(p.get("fieldname")))
        if liability:
            liability_data.append(liability[-2].get(p.get("fieldname")))
        if equity:
            equity_data.append(equity[-2].get(p.get("fieldname")))
        print("P is: ", p)


    datasets = []
    if asset_data:
        datasets.append({'name': _('Assets'), 'values': asset_data})
    if liability_data:
        datasets.append({'name': _('Liabilities'), 'values': liability_data})
    if equity_data:
        datasets.append({'name': _('Equity'), 'values': equity_data})

    chart = {
        "data": {
            'labels': labels,
            'datasets': datasets
        }
    }

    chart["type"] = "bar"

    return chart
