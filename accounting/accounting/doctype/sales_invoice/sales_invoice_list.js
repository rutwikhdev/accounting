frappe.listview_settings['Sales Invoice'] = {
    // called on every reload.
    get_indicator(doc) {
        if (doc.status == 'Unpaid') {
            return [__('Unpaid'), 'orange']
        } else if (doc.status == 'Paid') {
            return [__('Paid'), 'green']
        } else if (doc.status == 'Overdue') {
            return [__('Overdue'), 'red']
        }
    }
}