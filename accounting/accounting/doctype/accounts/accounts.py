# Copyright (c) 2021, Rutwik and contributors
# For license information, please see license.txt

# import frappe
from frappe.utils.nestedset import NestedSet

class Accounts(NestedSet):
	def autoname(self):
		self.name = self.account_name
