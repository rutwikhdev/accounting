# Copyright (c) 2021, Rutwik and contributors
# For license information, please see license.txt

import frappe, os, json
from frappe.utils import cstr
from unidecode import unidecode
from six import iteritems
from frappe.utils.nestedset import rebuild_tree
from frappe.model.document import Document

class ChartofAccountsImporter(Document):
    pass

@frappe.whitelist()
def import_coa(file_name):
    print('IMPORTTTTTTTCOAAAAAAAAa')
    file_doc = frappe.get_doc("File", {"file_url": file_name})
    _, extension = file_doc.get_extension()

    if 'json' not in extension:
        frappe.throw('Only JSON files please!')

    data = generate_tree(file_doc)
    create_charts(custom_chart=data)

def generate_tree(file_doc):
    file_path = file_doc.get_full_path()

    with open(file_path, 'r') as j:
        chart = json.loads(j.read())

    return chart

def identify_is_group(child):
    if child.get("is_group"):
        is_group = child.get("is_group")
    elif len(set(child.keys()) - set(["account_type", "root_type", "is_group", "tax_rate", "account_number"])):
        is_group = 1
    else:
        is_group = 0

    return is_group

def add_suffix_if_duplicate(account_name, account_number, accounts):
    if account_number:
        account_name_in_db = unidecode(" - ".join([account_number,
                                                   account_name.strip().lower()]))
        print(account_name, account_number, accounts, account_name_in_db)
    else:
        account_name_in_db = unidecode(account_name.strip().lower())
        print(account_name_in_db)

    if account_name_in_db in accounts:
        count = accounts.count(account_name_in_db)
        account_name = account_name + " " + cstr(count)

    return account_name, account_name_in_db

def create_charts(chart_template=None, custom_chart=None):
    chart = custom_chart or get_chart(chart_template)
    if chart:
        accounts = []

        def _import_accounts(children, parent, root_type, root_account=False):
            '''Scanning the entries created Account doctype'''
            for account_name, child in iteritems(children):
                if root_account:
                    root_type = child.get("root_type")

                if account_name not in ["account_number", "account_type",
                                        "root_type", "is_group", "tax_rate"]:

                    account_number = cstr(child.get("account_number")).strip()
                    account_name, account_name_in_db = add_suffix_if_duplicate(account_name,
                                                                               account_number, accounts)

                    is_group = identify_is_group(child)
                    report_type = "Balance Sheet" if root_type in ["Asset", "Liability", "Equity"] \
                else "Profit and Loss"

                    account = frappe.get_doc({
                        "doctype": "Accounts",
                        "account_name": account_name,
                        "parent_accounts": parent,
                        "is_group": is_group,
                        "root_type": root_type,
                        "report_type": report_type,
                        "account_number": account_number,
                        "account_type": child.get("account_type"),
                    })

                    #if root_account or frappe.local.flags.allow_unverified_charts:
                    account.flags.ignore_mandatory = True
                    account.flags.ignore_permissions = True
                    account.insert()
                    accounts.append(account_name_in_db)
                    _import_accounts(child, account.name, root_type)

        # Rebuild NestedSet HSM tree for Account Doctype
        # after all accounts are already inserted.
        frappe.local.flags.ignore_update_nsm = True
        _import_accounts(chart, None, None, root_account=True)
        rebuild_tree("Accounts", "parent_accounts")
        frappe.local.flags.ignore_update_nsm = False

