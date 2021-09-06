// Copyright (c) 2016, Rutwik and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Profit and Loss"] = {
    "filters": [
        {
            'fieldname': 'from_date',
            'label': __('From Date'),
            'fieldtype': 'Date',
            'reqd': 1
        },
        {
            'fieldname': 'to_date',
            'label': __('To Date'),
            'fieldtype': 'Date',
            'reqd': 1
        }

    ]
};
