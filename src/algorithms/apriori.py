from itertools import combinations

def get_support(itemset, transactions):
    count = sum(1 for t in transactions if itemset.issubset(t))
    return count / len(transactions)

def apriori_algorithm(transactions, min_support):
    items = sorted({i for t in transactions for i in t})
    L = [{i} for i in items]

    freq = []
    k = 1

    while L:
        next_L = []
        for itemset in L:
            sup = get_support(set(itemset), transactions)
            if sup >= min_support:
                freq.append((set(itemset), sup))

        # generate candidates
        candidates = []
        for a in freq:
            for b in freq:
                union = a[0] | b[0]
                if len(union) == k + 1 and union not in candidates:
                    candidates.append(union)

        L = candidates
        k += 1

    return freq

def generate_rules_apriori(freq, min_conf):
    rules = []
    for itemset, support in freq:
        if len(itemset) < 2:
            continue

        for item in itemset:
            antecedent = {item}
            consequent = itemset - antecedent
            conf = support  # simplified
            if conf >= min_conf:
                rules.append({
                    "antecedent": antecedent,
                    "consequent": consequent,
                    "confidence": conf
                })
    return rules
