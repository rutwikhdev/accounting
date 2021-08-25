#Copyright (c) 2021, Rutwik and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class SalesInvoice(Document):
    def validate(self):
        self.set_status()
        self.set_total_amount()

    def on_submit(self):
        self.make_gl_entries()

    def on_cancel(self):
        self.make_reverse_gl_entries()

    def set_total_amount(self):
        self.grand_total = 0
        # for item in self.items:
        #     self.grand_total += item.rate * item.quantity
        self.grand_total = sum([item.amount for item in self.items])

        print(self.grand_total)
        print(flt(self.grand_total, 3))

    def set_status(self):
        '''
        self.docstatus

        Draft: 0
        Submitted: 1, Paid or Unpaid or Overdue
        Cancelled: 2
        '''
        if self.is_new():
            if self.get('amended_form'):
                self.status = 'Draft'
            return
        print('Status', self.docstatus)
        if self.docstatus == 1:
            # outstanding_amount > amount_paid and due_date < now_date: status = 'Overdue'
            # outstanding_amount > amount_paid and due_date > now_date: status = 'Unpaid'
            # outstanding_amount <= amount_paid: status = 'Paid'
            self.status = 'Unpaid'
            print('Unpaid')

    def on_submit(self):
        self.make_gl_entries()

    def on_cancel(self):
        self.make_reverse_gl_entries()

    def make_gl_entries(self):
        # Credit
        c_gl = frappe.new_doc('GL Entry')
        c_gl.posting_date = self.date
        c_gl.account = self.credit_from
        c_gl.credit = self.grand_total
        c_gl.debit = flt(0)
        c_gl.submit()

        # Debit
        d_gl = frappe.new_doc('GL Entry')
        d_gl.posting_date = self.date
        d_gl.account = self.debit_to
        d_gl.debit = self.grand_total
        d_gl.credit = flt(0)
        d_gl.submit()

    def make_reverse_gl_entries(self):
        '''Ledger is immutable hence we need to make reverse entries for '''
        # Credit
        c_gl = frappe.new_doc('GL Entry')
        c_gl.posting_date = self.date
        c_gl.account = 'Debtors'
        c_gl.credit = self.grand_total
        c_gl.debit = flt(0)
        c_gl.submit()

        # Debit
        d_gl = frappe.new_doc('GL Entry')
        c_gl.posting_date = self.date
        d_gl.account = 'Some Credit acc'
        d_gl.debit = self.grand_total
        d_gl.credit = flt(0)
        d_gl.credit.submit()
