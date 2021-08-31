#Copyright (c) 2021, Rutwik and contributors
# For license information, please see license.txt

from frappe.model.document import Document
from ..gl_entry.gl_entry import make_gl_entries

class SalesInvoice(Document):
    def validate(self):
        self.set_status()
        self.set_total_amount()

    def set_total_amount(self):
        self.grand_total = 0
        self.grand_total = sum(item.amount for item in self.items)

    def set_status(self):
        '''
        Draft: 0
        Submitted: 1, Paid or Unpaid or Overdue
        Cancelled: 2
        '''
        if self.is_new():
            if self.get('amended_form'):
                self.status = 'Draft'
            return
        
        if self.docstatus == 1:
            self.status = 'Unpaid'

    def on_submit(self):
        kwargs = {
            'date': self.date,
            'debit_acc': self.debit_to,
            'credit_acc': self.credit_from,
            'amount': self.grand_total,
            'voucher_type': 'Sales Invoice',
            'voucher_no': self.name,
            'against_voucher_type': '',
            'against_voucher_no': ''
        }
        make_gl_entries(**kwargs)

    def on_cancel(self):
        kwargs = {
            'date': self.date,
            'debit_acc': self.debit,
            'credit_acc': self.credit_form,
            'amount': self.grand_total,
            'voucher_type': 'Sales Invoice',
            'voucher_no': self.name,
            'against_voucher_type': "",
            'against_voucher_no': "",
            'reverse': True
        }
        make_gl_entries(**kwargs)