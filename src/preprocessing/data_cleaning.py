def preprocess_data(transactions, valid_products):
    cleaned = []
    empty = 0
    single = 0
    duplicates = 0
    invalid = 0

    for tx in transactions:
        if len(tx) == 0:
            empty += 1
            continue

        tx = [item.strip().lower() for item in tx]

        # remove duplicates
        before = len(tx)
        tx = list(set(tx))
        duplicates += before - len(tx)

        # remove invalid
        valid_tx = [i for i in tx if i in valid_products]
        invalid += len(tx) - len(valid_tx)

        if len(valid_tx) <= 1:
            single += 1
            continue

        cleaned.append(valid_tx)

    report = {
        "Empty Removed": empty,
        "Single-item Removed": single,
        "Duplicates Removed": duplicates,
        "Invalid Items Removed": invalid,
        "Final Transactions": len(cleaned)
    }

    return cleaned, report
