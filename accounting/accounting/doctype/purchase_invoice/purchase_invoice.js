// Copyright (c) 2021, Rutwik and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice', {
	// refresh: function(frm) {

	// }
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