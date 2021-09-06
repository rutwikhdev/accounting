# Copyright (c) 2021, Rutwik and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ..gl_entry.gl_entry import make_gl_entries

class PaymentEntry(Document):
    def validate(self):
        if self.payment_type == 'Receive': # Sales Invoice
            ac = frappe.get_doc('Accounts', self.account)
            if not ac.root_type == 'Income':
                frappe.throw('The account should be of type Income')
        elif self.payment_type == 'Pay': # Purchase Invoice
            ac = frappe.get_doc('Accounts', self.account)
            print(ac.root_type)
            if not ac.root_type == 'Expense':
                frappe.throw('The account should be of type Expense')
        else:
            frappe.throw('Invalid payment entry, need a Sales or Purchase Invoice')

    def set_status(self, status):
        doctype = 'Sales Invoice' if self.payment_type == 'Receive' else 'Purchase Invoice'
        docname = self.sales_invoice if self.payment_type == 'Receive' else self.purchase_invoice

        iv = frappe.get_doc(doctype, docname)
        iv.status = status
        iv.save()

    def on_submit(self):
        kwargs = {
            'date': self.posting_date,
            'debit_acc': self.account,
            'credit_acc': self.paid_to_s if self.payment_type == 'Receive' else self.paid_to_p,
            'amount': self.paid_amount_s if self.payment_type == 'Receive' else self.paid_amount_p,
            'voucher_type': 'Payment Entry',
            'voucher_no': self.name,
            'against_voucher_type': 'Sales Invoice' if self.payment_type == 'Receive' else 'Purchase Invoice',
            'against_voucher_no': self.sales_invoice if self.payment_type == 'Receive' else self.purchase_invoice
        }
        make_gl_entries(**kwargs)
        self.set_status('Paid')

    def on_cancel(self):
        kwargs = {
            'date': self.posting_date,
            'debit_acc': self.account,
            'credit_acc': self.paid_to_s if self.payment_type == 'Receive' else self.paid_to_p,
            'amount': self.paid_amount_s if self.payment_type == 'Receive' else self.paid_amount_p,
            'voucher_type': 'Payment Entry',
            'voucher_no': self.name,
            'against_voucher_type': 'Sales Invoice' if self.payment_type == 'Receive' else 'Purchase Invoice',
            'against_voucher_no': self.sales_invoice if self.payment_type == 'Receive' else self.purchase_invoice,
            'reverse': True
        }
        make_gl_entries(**kwargs)
        self.set_status('Unpaid')
