import streamlit as st
import pandas as pd

# Title and Introduction
st.title("🔄 Transactions")
st.markdown("""
Welcome to the SQL Transactions tutorial! 🚀

Transactions are sequences of SQL statements that are executed as a single unit of work. They ensure the database remains consistent and reliable.

---

### What We'll Cover:
1. **ACID Properties**: Atomicity, Consistency, Isolation, Durability.
2. **COMMIT and ROLLBACK**.
3. **SAVEPOINT**.
4. **Transaction Isolation Levels**.
5. **Locking Mechanisms**.

---

Here’s a sample table to demonstrate these concepts:
""")

# Sample Data
products = pd.DataFrame({
    'product_id': [1, 2, 3],
    'product_name': ['Laptop', 'Phone', 'Tablet'],
    'stock': [10, 15, 8],
    'price': [1000, 500, 300]
})

st.subheader("Product Table")
st.dataframe(products)

# Tabs for Subtopics
tabs = st.tabs([
    "ACID Properties", "COMMIT and ROLLBACK", "SAVEPOINT",
    "Transaction Isolation Levels", "Locking Mechanisms"
])

# ACID Properties
with tabs[0]:
    st.header("🔹 ACID Properties")
    st.markdown("""
    **ACID** properties ensure reliable transaction processing:
    
    1. **Atomicity**: All operations in a transaction are completed, or none are.
    2. **Consistency**: Ensures the database transitions from one valid state to another.
    3. **Isolation**: Transactions do not interfere with each other.
    4. **Durability**: Once committed, changes persist even in case of a system failure.
    
    ### Interactive Example:
    Simulate an atomic transaction to update the stock for a product.
    """)

    product_to_update = st.selectbox("Select a Product:", products['product_name'])
    stock_update = st.number_input("Enter Stock to Deduct (Atomic Operation):", min_value=1, value=1)

    if st.button("Perform Transaction"):
        product_row = products[products['product_name'] == product_to_update].copy()
        if stock_update > product_row['stock'].iloc[0]:
            st.error("❌ Transaction Failed: Insufficient stock!")
        else:
            products.loc[products['product_name'] == product_to_update, 'stock'] -= stock_update
            st.success(f"✅ Transaction Successful! Updated stock for {product_to_update}.")
        st.dataframe(products)

# COMMIT and ROLLBACK
if "transaction_products" not in st.session_state:
    st.session_state.transaction_products = products.copy()

with tabs[1]:
    st.header("🔧 COMMIT and ROLLBACK")
    st.markdown("""
    **COMMIT**: Permanently saves all changes made in the current transaction.
    
    **ROLLBACK**: Undoes changes made during the current transaction.
    
    ### Interactive Example:
    Simulate a transaction with COMMIT and ROLLBACK options.
    """)

    st.markdown("### Update Stock and Choose to COMMIT or ROLLBACK")
    transaction_stock_update = st.number_input(
        "Enter Laptop Stock to Deduct:", min_value=1, value=1, key="commit_rollback_stock"
    )

    if st.button("Start Transaction"):
        if transaction_stock_update > st.session_state.transaction_products.loc[0, 'stock']:
            st.error("❌ Transaction Failed: Insufficient stock!")
        else:
            st.session_state.transaction_products.loc[0, 'stock'] -= transaction_stock_update
            st.markdown("Transaction in Progress... Choose an action:")
            st.dataframe(st.session_state.transaction_products)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("COMMIT Transaction"):
            products.update(st.session_state.transaction_products)
            st.success("✅ Transaction Committed! Changes saved permanently.")
            st.dataframe(products)

    with col2:
        if st.button("ROLLBACK Transaction"):
            st.session_state.transaction_products = products.copy()
            st.warning("↩️ Transaction Rolled Back! No changes were made.")
            st.dataframe(products)

# SAVEPOINT
if "savepoint_products" not in st.session_state:
    st.session_state.savepoint_products = products.copy()

with tabs[2]:
    st.header("🔖 SAVEPOINT")
    st.markdown("""
    **SAVEPOINT** allows setting intermediate checkpoints within a transaction.
    
    **SQL Syntax**:
    ```sql
    SAVEPOINT savepoint_name;
    ROLLBACK TO savepoint_name;
    ```
    
    ### Interactive Example:
    Create a SAVEPOINT during a transaction and ROLLBACK to it.
    """)

    st.markdown("### Simulate a SAVEPOINT")
    savepoint_stock_update = st.number_input(
        "Enter Laptop Stock to Deduct at SAVEPOINT:", min_value=1, value=1, key="savepoint_stock"
    )

    if st.button("Start Transaction with SAVEPOINT"):
        if savepoint_stock_update > st.session_state.savepoint_products.loc[0, 'stock']:
            st.error("❌ Transaction Failed: Insufficient stock!")
        else:
            st.session_state.savepoint_products.loc[0, 'stock'] -= savepoint_stock_update
            st.markdown("Savepoint Created! Current Table:")
            st.dataframe(st.session_state.savepoint_products)

    if st.button("ROLLBACK to Savepoint"):
        st.session_state.savepoint_products = products.copy()
        st.warning("↩️ Rolled Back to Savepoint!")
        st.dataframe(products)

# Transaction Isolation Levels
with tabs[3]:
    st.header("🔒 Transaction Isolation Levels")
    st.markdown("""
    Isolation levels control the interaction between concurrent transactions:
    """)

    isolation_level = st.selectbox("Select Isolation Level:", [
        "Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable"
    ])
    if isolation_level == "Read Uncommitted":
        st.warning("Transactions can read uncommitted data, leading to dirty reads.")
    elif isolation_level == "Read Committed":
        st.info("Only committed data is visible to transactions, preventing dirty reads.")
    elif isolation_level == "Repeatable Read":
        st.success("Ensures consistent data for a transaction, preventing non-repeatable reads.")
    elif isolation_level == "Serializable":
        st.success("Provides the highest level of isolation, transactions execute sequentially avoiding all concurrency issues.")

# Locking Mechanisms
with tabs[4]:
    st.header("🔐 Locking Mechanisms")
    st.markdown("""
    Locks prevent multiple transactions from conflicting with each other:
    
    **Example**: Simulate a shared lock on a product.
    """)

    product_to_lock = st.selectbox("Select a Product to Lock:", products['product_name'])
    lock_type = st.radio("Select Lock Type:", ["Shared Lock", "Exclusive Lock"])

    if lock_type == "Shared Lock":
        st.info(f"🔓 Shared Lock: {product_to_lock} is read-only during the lock.")
    elif lock_type == "Exclusive Lock":
        st.warning(f"🔒 Exclusive Lock: {product_to_lock} is locked for all operations.")

# Footer Quiz Section
st.markdown("---")
st.header("🎯 Test Your Knowledge!")
quiz_question = st.multiselect(
    "Which of the following statements about transactions are true? (Select all that apply)",
    [
        "COMMIT makes changes permanent.",
        "ROLLBACK undoes all changes since the last COMMIT.",
        "SAVEPOINT allows rolling back to intermediate states.",
        "Read Uncommitted is the highest isolation level."
    ],
    key="quiz_transactions"
)

if st.button("Submit Answer", key="quiz_submit_transactions"):
    correct_answers = {
        "COMMIT makes changes permanent.",
        "ROLLBACK undoes all changes since the last COMMIT.",
        "SAVEPOINT allows rolling back to intermediate states."
    }
    selected_answers = set(quiz_question)

    if selected_answers == correct_answers:
        st.success("Correct! 🎉 Transactions help maintain database reliability.")
    else:
        missing = correct_answers - selected_answers
        extra = selected_answers - correct_answers
        feedback = "Oops! Here's what you missed:\n"
        if missing:
            feedback += f"- Missing correct answer(s): {', '.join(missing)}\n"
        if extra:
            feedback += f"- Incorrect answer(s): {', '.join(extra)}\n"
        st.error(feedback)

# Footer Section
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin-top: 20px;">
    Queries @ 
    <a href="mailto:riyabasu06@gmail.com" style="text-decoration: none; color: #2e77d0;">
        <strong>❤️Riya Bose❤️</strong>
    </a>
</div>
""", unsafe_allow_html=True)