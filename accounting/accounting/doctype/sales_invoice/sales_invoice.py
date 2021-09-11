#Copyright (c) 2021, Rutwik and contributors
# For license information, please see license.txt

import frappe, json, datetime
from frappe.utils import getdate
from frappe.model.document import Document
from accounting.accounting.doctype.gl_entry.gl_entry import make_gl_entries

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

@frappe.whitelist(allow_guest=True)
def generate_sales_invoice(data):
    data = json.loads(data)
    items = []

    for item in data:
        rate = frappe.db.get_value('Item', item['itemName'], 'price')
        qty = int(item['quantity'])
        items.append(frappe._dict({
            'item': item['itemName'], 'quantity': qty, 'rate': rate, 'amount': rate * qty
        }))

    frappe.get_doc({
        'doctype': 'Sales Invoice',
        'customer_name': 'E Store Customer',
        'due_date': getdate() + datetime.timedelta(days=7),
        'debit_to': 'Debtors',
        'credit_from': 'Stock In Hand',
        'items': items,
        'status': 'Unpaid'
    }).submit()


    return "returning invoice"
