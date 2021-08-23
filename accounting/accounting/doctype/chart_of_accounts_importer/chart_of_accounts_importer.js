// Copyright (c) 2021, Rutwik and contributors
// For license information, please see license.txt

frappe.ui.form.on('Chart of Accounts Importer', {
    onload: function(frm) {
        frm.set_value("import_file", "")
    },
    refresh: function(frm) {
        frm.disable_save()
        create_btn(frm)
    }
});

var create_btn = (frm) => {
    frm.page.set_primary_action(__("Import"), function () {
        frappe.call({
            method: "accounting.accounting.doctype.chart_of_accounts_importer.chart_of_accounts_importer.import_coa",
            args: {
                file_name: frm.doc.import_file,
            },
            freeze: true,
            callback: function(r) {
                console.log('Btn func!')
            }
        });
    }).addClass('btn btn-primary');
}

