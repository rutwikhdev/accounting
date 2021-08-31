// Copyright (c) 2021, Rutwik and contributors
// For license information, please see license.txt

frappe.ui.form.on('Payment Entry', {
    refresh: function(frm) {
        frm.set_query('sales_invoice', () => {
            return {
                'filters': {'status': 'Unpaid'}
            }
        });
        frm.set_query('purchase_invoice', () => {
            return {
                'filters': {'status': 'Unpaid'}
            }
        });
    },
});
