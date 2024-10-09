# 勘定科目の推測
def guess_accounting_subject(store_name, subjects):
    for key, subject in subjects.items():
        if key in store_name:
            return subject
    return "その他"


# 軽減税率の推測
def guess_reduced_tax_rate(store_name, reduced_tax_stores):
    for store in reduced_tax_stores:
        if store in store_name:
            return "※"
    return ""
