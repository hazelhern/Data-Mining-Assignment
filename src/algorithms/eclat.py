def eclat_algorithm(transactions, min_support):
    tid_sets = {}

    for tid, tx in enumerate(transactions):
        for item in tx:
            if item not in tid_sets:
                tid_sets[item] = set()
            tid_sets[item].add(tid)

    freq = []

    items = list(tid_sets.items())

    def dfs(prefix, items):
        for i in range(len(items)):
            item, tids = items[i]
            new_prefix = prefix | {item}
            sup = len(tids) / len(transactions)

            if sup >= min_support:
                freq.append((new_prefix, sup))
                suffix = []
                for j in range(i + 1, len(items)):
                    item2, tids2 = items[j]
                    inter = tids & tids2
                    if inter:
                        suffix.append((item2, inter))
                dfs(new_prefix, suffix)

    dfs(set(), items)
    return freq

def generate_rules_eclat(freq, min_conf):
    rules = []
    for itemset, support in freq:
        if len(itemset) < 2:
            continue

        for item in itemset:
            rules.append({
                "antecedent": {item},
                "consequent": itemset - {item},
                "confidence": support
            })
    return rules
