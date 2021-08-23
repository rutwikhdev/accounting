#Copyright (c) 2021, Rutwik and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class SalesInvoice(Document):
    def validate(self):
        self.status_update()
        print(self.items)
        self.set_total_amount()

    def on_submit(self):
        self.make_gl_entries()

    def on_cancel(self):
        self.make_reverse_gl_entries()

    def set_total_amount(self):
        self.grand_total = 0
        for item in self.items:
            self.grand_total += item.rate * item.quantity

        print(self.grand_total)
        print(flt(self.grand_total, 3))

    def status_update(self):
        '''
        self.docstatus

        Draft: 0
        Submitted: 1
        Cancelled: 2
        '''
        if self.is_new():
            if self.get('amended_form'):
                self.status('Draft')
            return
        # if self.docstatus == 1:
            # self.make_gl_entries()
        # elif self.docstatus == 2:
            # self.make_reverse_gl_entries()

    def on_submit(self):
        self.make_gl_entries()

    def on_cancel(self):
        self.make_reverse_gl_entries()

    def make_gl_entries(self):
        # Credit
        c_gl = frappe.new_doc('GL Entry')
        c_gl.posting_date = self.date
        c_gl.account = 'Some Credit acc'
        c_gl.credit = self.grand_total
        c_gl.debit = flt(0)
        c_gl.submit()

        # Debit
        d_gl = frappe.new_doc('GL Entry')
        d_gl.posting_date = self.date
        d_gl.account = 'Debtors'
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
