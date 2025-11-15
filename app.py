import streamlit as st
import pandas as pd
import time

from src.preprocessing.data_cleaning import preprocess_data
from src.algorithms.apriori import apriori_algorithm, generate_rules_apriori
from src.algorithms.eclat import eclat_algorithm, generate_rules_eclat

st.set_page_config(page_title="Supermarket Association Mining", layout="wide")

st.title("Supermarket Simulator")

# Load products
@st.cache_data
def load_products():
    # Accept comma OR tab separated rows
    df = pd.read_csv("data/products.csv", sep=r'\s*,\s*|\t+', engine="python", header=0)

    # Normalize product names
    df["product_name"] = df["product_name"].astype(str).str.strip().str.lower()

    return df

products_df = load_products()
product_list = list(products_df["product_name"].unique())


# SHOPPING SYSTEM UI
st.header("Create or Import Transactions")

tab1, tab2 = st.tabs(["Manual Creation", "Upload CSV"])

if "transactions" not in st.session_state:
    st.session_state["transactions"] = []

transactions = st.session_state["transactions"]

# Manual Creation
with tab1:
    st.subheader("Create Transaction")

    selected = st.multiselect("Select products:", product_list)

    if st.button("Add Transaction"):
        if len(selected) > 0:
            transactions.append(selected)
            st.session_state["transactions"] = transactions
            st.success(f"Transaction added: {selected}")
        else:
            st.warning("Please select at least one product.")

    st.write("### Current Transactions:")
    st.table(transactions)


# CSV Upload
with tab2:
    st.subheader("Upload Transaction CSV")
    uploaded = st.file_uploader("Upload sample_transactions.csv", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)

        st.write("CSV Columns:", df.columns.tolist())
        item_column = df.columns[-1]  # last column contains items

        df[item_column] = df[item_column].fillna("")

        # Clean + normalize transaction strings
        transactions = df[item_column].apply(
            lambda x: [
                item.strip().lower()
                for item in str(x).split(",")
                if item.strip() != ""
            ]
        ).tolist()

        st.session_state["transactions"] = transactions

        st.success(f"Loaded {len(transactions)} raw transactions.")


# PREPROCESSING
st.header("Data Preprocessing")

if st.button("Run Preprocessing"):
    clean_tx, report = preprocess_data(transactions, product_list)

    st.success("Preprocessing complete!")
    st.json(report)

    # Preprocessing summary statistics
    before_total = len(transactions)
    before_items = sum(len(t) for t in transactions)
    before_avg = before_items / before_total if before_total > 0 else 0
    before_unique = len(set(item for t in transactions for item in t))

    st.write("### Before Cleaning Stats:")
    st.json({
        "Total Transactions": before_total,
        "Total Items": before_items,
        "Avg Items per Transaction": round(before_avg, 2),
        "Unique Items": before_unique
    })

    after_total = len(clean_tx)
    after_items = sum(len(t) for t in clean_tx)
    after_avg = after_items / after_total if after_total > 0 else 0
    after_unique = len(set(item for t in clean_tx for item in t))

    st.write("### After Cleaning Stats:")
    st.json({
        "Total Clean Transactions": after_total,
        "Total Items": after_items,
        "Avg Items per Transaction": round(after_avg, 2),
        "Unique Items": after_unique
    })

    st.write("### Cleaned Transactions:")
    st.table(clean_tx)

    st.session_state["cleaned"] = clean_tx


# MINING ALGORITHMS
st.header("Association Rule Mining")

if "cleaned" in st.session_state and len(st.session_state["cleaned"]) > 0:

    min_sup = st.slider("Minimum Support (%)", 1, 50, 20) / 100
    min_conf = st.slider("Minimum Confidence (%)", 10, 90, 50) / 100

    if st.button("Run Apriori + Eclat"):
        clean_tx = st.session_state["cleaned"]

        # APRIORI
        start = time.time()
        freq_ap = apriori_algorithm(clean_tx, min_sup)
        rules_ap = generate_rules_apriori(freq_ap, min_conf)
        apriori_time = (time.time() - start) * 1000

        # ECLAT
        start = time.time()
        freq_ec = eclat_algorithm(clean_tx, min_sup)
        rules_ec = generate_rules_eclat(freq_ec, min_conf)
        eclat_time = (time.time() - start) * 1000

        st.session_state["rules_ap"] = rules_ap
        st.session_state["rules_ec"] = rules_ec

        st.success("Mining Completed!")

        st.write("### Apriori Rules")
        st.write(rules_ap)

        st.write("### Eclat Rules")
        st.write(rules_ec)

        perf_df = pd.DataFrame({
            "Algorithm": ["Apriori", "Eclat"],
            "Time (ms)": [round(apriori_time, 2), round(eclat_time, 2)],
            "Rules Generated": [len(rules_ap), len(rules_ec)],
        })

        st.write("### Performance Comparison")
        st.table(perf_df)


else:
    st.warning("Please preprocess the dataset first!")


# RECOMMENDATION SYSTEM
st.header("Product Recommendation System")

if "rules_ap" in st.session_state:

    chosen = st.selectbox("Select product:", product_list)

    rules_ap = st.session_state["rules_ap"]

    # collect rules with this antecedent
    matching_rules = []
    for rule in rules_ap:
        if rule["antecedent"] == {chosen}:
            matching_rules.append(rule)

    best_rules = {}
    for r in matching_rules:
        consequent = list(r["consequent"])[0]
        conf = r["confidence"]

        # keep highest confidence rule for each consequent item
        if consequent not in best_rules or conf > best_rules[consequent]["confidence"]:
            best_rules[consequent] = r

    # convert dict → list
    final_recommendations = list(best_rules.values())

    if final_recommendations:
        st.write(f"### Customers who bought **{chosen}** also bought:")

        for r in final_recommendations:
            conf_pct = int(r["confidence"] * 100)
            consequent_item = list(r["consequent"])[0]
            st.write(f"- **{consequent_item}** — {conf_pct}%")

    else:
        st.info("No recommendations found for this product.")

    st.write("### Business Insights")

    if final_recommendations:
        top_item = final_recommendations[0]
        consequent_item = list(top_item['consequent'])[0]
        conf_pct = int(top_item["confidence"] * 100)

        st.success(
            f"**Business Strategy Suggestion:**\n\n"
            f"Place **{chosen.capitalize()}** close to **{consequent_item.capitalize()}** in the store.\n"
            f"This combination appears in {conf_pct}% of relevant transactions, indicating a strong "
            f"association and an opportunity for cross-selling."
        )
    else:
        st.info("No strong associations found for business recommendation.")
