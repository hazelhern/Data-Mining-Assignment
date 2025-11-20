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
    df = pd.read_csv("data/products.csv", sep=r'\s*,\s*|\t+', engine="python", header=0)
    df["product_name"] = df["product_name"].astype(str).str.strip().str.lower()
    return df

products_df = load_products()
product_list = list(products_df["product_name"].unique())


# Transaction
st.header("Create or Import Transactions")

tab1, tab2 = st.tabs(["Manual Creation", "Upload CSV"])

if "transactions" not in st.session_state:
    st.session_state["transactions"] = []

transactions = st.session_state["transactions"]

# Manual
with tab1:
    st.subheader("Create Transaction")
    selected = st.multiselect("Select products:", product_list)

    if st.button("Add Transaction"):
        if selected:
            transactions.append(selected)
            st.session_state["transactions"] = transactions
            st.success("Transaction added!")
        else:
            st.warning("Please select at least one product.")

    st.write("### Current Transactions")
    st.table(transactions)

# Upload
with tab2:
    uploaded = st.file_uploader("Upload sample_transactions.csv", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        item_col = df.columns[-1]
        df[item_col] = df[item_col].fillna("")
        transactions = df[item_col].apply(
            lambda x: [item.strip().lower() for item in str(x).split(",") if item.strip()]
        ).tolist()

        st.session_state["transactions"] = transactions
        st.success(f"Loaded {len(transactions)} raw transactions.")


# PREPROCESSING
st.header("Data Preprocessing")

if st.button("Run Preprocessing"):
    clean_tx, report = preprocess_data(transactions, product_list)

    st.session_state["cleaned"] = clean_tx
    st.session_state["clean_report"] = report

# Show preprocessing results if available
if "cleaned" in st.session_state:
    st.success("Preprocessing complete!")
    st.json(st.session_state["clean_report"])

    # Stats Before
    before_total = len(transactions)
    before_items = sum(len(t) for t in transactions)
    before_unique = len(set(i for t in transactions for i in t))

    st.write("### Before Cleaning Stats")
    st.json({
        "Total Transactions": before_total,
        "Avg Items per Transaction": round(before_items / max(1, before_total), 2),
        "Unique Items": before_unique
    })

    # Stats After
    clean_tx = st.session_state["cleaned"]
    after_total = len(clean_tx)
    after_items = sum(len(t) for t in clean_tx)
    after_unique = len(set(i for t in clean_tx for i in t))

    st.write("### After Cleaning Stats")
    st.json({
        "Total Clean Transactions": after_total,
        "Avg Items per Transaction": round(after_items / max(1, after_total), 2),
        "Unique Items": after_unique
    })

    st.write("### Cleaned Transactions")
    st.table(clean_tx)
else:
    st.info("Please preprocess the dataset before mining.")



# MINING ALGORITHMS
st.header("Association Rule Mining")

if "cleaned" in st.session_state and len(st.session_state["cleaned"]) > 0:

    algo_choice = st.selectbox(
        "Choose Algorithm:",
        ["Apriori", "Eclat"]
    )

    min_sup = st.slider("Minimum Support (%)", 1, 50, 20) / 100
    min_conf = st.slider("Minimum Confidence (%)", 10, 90, 50) / 100

    if st.button("Run Algorithm"):
        clean_tx = st.session_state["cleaned"]

        if algo_choice == "Apriori":
            start = time.time()
            freq = apriori_algorithm(clean_tx, min_sup)
            rules = generate_rules_apriori(freq, min_conf)
            runtime = (time.time() - start) * 1000

        elif algo_choice == "Eclat":
            start = time.time()
            freq = eclat_algorithm(clean_tx, min_sup)
            rules = generate_rules_eclat(freq, min_conf)
            runtime = (time.time() - start) * 1000

        st.session_state["rules"] = rules

        st.success(f"{algo_choice} Completed!")
        st.write(f"### {algo_choice} Rules")
        st.write(rules)

        st.write("### Performance")
        st.json({
            "Runtime (ms)": round(runtime, 2),
            "Rules Generated": len(rules)
        })


# RECOMMENDATION SYSTEM
st.header("Product Recommendation System")

if "rules" in st.session_state:

    chosen = st.selectbox("Select product for recommendation:", product_list)
    rules = st.session_state["rules"]

    # Find rules where antecedent is the chosen item
    matching_rules = []
    for rule in rules:
        antecedent = rule["antecedent"]
        if len(antecedent) == 1 and chosen in antecedent:
            matching_rules.append(rule)

    # Pick highest confidence rule per recommended item
    best_rules = {}
    for r in matching_rules:
        consequent_item = list(r["consequent"])[0]
        conf = r["confidence"]

        if consequent_item not in best_rules or conf > best_rules[consequent_item]["confidence"]:
            best_rules[consequent_item] = r

    final_recommendations = list(best_rules.values())

    if final_recommendations:
        st.write(f"### Customers who bought **{chosen}** also bought:")

        for r in final_recommendations:
            item = list(r["consequent"])[0]
            conf_pct = int(r["confidence"] * 100)
            st.write(f"- **{item}** — {conf_pct}% confidence")
    else:
        st.info("No recommendations found for this product using the selected algorithm.")

    # Business Insights
    st.write("### Business Insights")
    if final_recommendations:
        top = final_recommendations[0]
        item = list(top["consequent"])[0]
        conf_pct = int(top["confidence"] * 100)

        st.success(
            f"Place **{chosen.capitalize()}** near **{item.capitalize()}** on shelves.\n\n"
            f"This association appears in **{conf_pct}%** of matching transactions, indicating "
            f"a strong cross-selling opportunity."
        )
    else:
        st.info("No strong business insights available.")
else:
    st.warning("Run an association rule algorithm first!")