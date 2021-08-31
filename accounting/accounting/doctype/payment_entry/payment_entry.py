# Copyright (c) 2021, Rutwik and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class PaymentEntry(Document):
    def set_status(self, status):
        doctype = 'Sales Invoice' if self.payment_type == 'Receive' else 'Purchase Invoice'
        docname = self.sales_invoice if self.payment_type == 'Receive' else self.purchase_invoice

        iv = frappe.get_doc(doctype, docname)
        iv.status = status
        iv.save()

    def on_submit(self):
        paid_to = self.paid_to_s if self.payment_type == 'Receive' else self.paid_to_p
        self.make_gl_entries(self.account, paid_to)
        self.set_status('Paid')

    def on_cancel(self):
        paid_to = self.paid_to_s if self.payment_type == 'Receive' else self.paid_to_p
        self.make_gl_entries(self.account, paid_to, reverse=True)
        self.set_status('Unpaid')

    def make_gl_entries(self, debit_acc, credit_acc, reverse=False):
        if reverse:
            debit_acc, credit_acc = credit_acc, debit_acc

        # Debit
        d_gl = frappe.new_doc('GL Entry')
        d_gl.posting_date = self.posting_date
        d_gl.account = debit_acc
        d_gl.debit = self.paid_amount_s if self.payment_type == 'Receive' else self.paid_amount_p
        d_gl.credit = flt(0)
        d_gl.voucher_type = 'Payment Entry'
        d_gl.voucher_no = self.name
        d_gl.against_voucher_type = 'Sales Invoice' if self.payment_type == 'Receive' else self.paid_amount_p
        d_gl.against_voucher = self.sales_invoice if self.payment_type == 'Receive' else self.purchase_invoice
        d_gl.submit()

        # Credit
        c_gl = frappe.new_doc('GL Entry')
        c_gl.posting_date = self.posting_date
        c_gl.account = credit_acc
        c_gl.credit = self.paid_amount_s if self.payment_type == 'Receive' else self.paid_amount_p
        c_gl.debit = flt(0)
        c_gl.voucher_type = 'Payment Entry'
        c_gl.voucher_no = self.name
        c_gl.against_voucher_type = 'Sales Invoice' if self.payment_type == 'Receive' else 'Purchase Invoice'
        c_gl.against_voucher = self.sales_invoice if self.payment_type == 'Receive' else self.purchase_invoice
        c_gl.submit()
