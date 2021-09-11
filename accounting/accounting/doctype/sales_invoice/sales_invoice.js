// Copyright (c) 2021, Rutwik and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	refresh: function(frm) {
		frm.add_custom_button(__('Payment'), () => {
			const doc = frappe.model.get_new_doc('Payment Entry')
			frappe.set_route('Form', doc.doctype, doc.name)
		}, __('Create'))
	}
});

frappe.ui.form.on('Sales Invoice Item', {
	// cdt -> child Doctype
	// cdn -> child Docname
	rate(frm, cdt, cdn) {
		set_amount(frm, cdt, cdn);
	},
	quantity(frm, cdt, cdn) {
		set_amount(frm, cdt, cdn);
	}
});

function set_amount(frm, cdt, cdn) {
	let row = frappe.get_doc(cdt, cdn);
	row.amount = row.rate * row.quantity;
	frm.refresh()
}
