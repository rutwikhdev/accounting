# Copyright (c) 2021, Rutwik and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

class GLEntry(Document):
	pass

def make_gl_entries(date, debit_acc, credit_acc, amount, voucher_type, voucher_no, against_voucher_type=None, against_voucher_no=None, reverse=False):
	if reverse:
		debit_acc, credit_acc = credit_acc, debit_acc

	 # Debit
	frappe.get_doc({
		'doctype': 'GL Entry',
		'posting_date': date,
		'account': debit_acc,
		'debit': amount,
		'credit': flt(0),
		'voucher_type': voucher_type,
		'voucher_no': voucher_no,
		'against_voucher_type': against_voucher_type,
		'against_voucher': against_voucher_no,
	}).submit()

	# Credit
	frappe.get_doc({
		'doctype': 'GL Entry',
		'posting_date': date,
		'account': credit_acc,
		'credit': amount,
		'debit': flt(0),
		'voucher_type': voucher_type,
		'voucher_no': voucher_no,
		'against_voucher_type': against_voucher_type,
		'against_voucher': against_voucher_no,
	}).submit()