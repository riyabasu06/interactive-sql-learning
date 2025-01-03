import streamlit as st
import pandas as pd

# Title and Introduction
st.title("🔔 Triggers")
st.markdown("""
Welcome to the SQL Triggers tutorial! 🚀

A **trigger** is a stored program in the database that is automatically executed in response to specific events on a table.

---

### What We'll Cover:
1. **BEFORE Trigger**
2. **AFTER Trigger**
3. **INSTEAD OF Trigger**
4. **Trigger on INSERT, UPDATE, DELETE**
5. **Triggering Conditions (ROW vs. STATEMENT Level)**
6. **Dropping Triggers**

---

Here’s the sample data we’ll work with:
""")

# Sample Data
products = pd.DataFrame({
    'product_id': [1, 2, 3],
    'product_name': ['Laptop', 'Phone', 'Tablet'],
    'stock': [10, 15, 8],
    'price': [1000, 500, 300]
})

audit_log = pd.DataFrame(columns=['action', 'product_id', 'timestamp'])

st.subheader("Product Table")
st.dataframe(products)

st.subheader("Audit Log Table (Initially Empty)")
st.dataframe(audit_log)

# Tabs for Subtopics
tabs = st.tabs([
    "BEFORE Trigger", "AFTER Trigger", "INSTEAD OF Trigger", 
    "INSERT/UPDATE/DELETE", "Triggering Conditions", "Dropping Triggers"
])

# BEFORE Trigger
with tabs[0]:
    st.header("🔹 BEFORE Trigger")
    st.markdown("""
    **Definition**: A `BEFORE` trigger executes before an `INSERT`, `UPDATE`, or `DELETE` operation on a table.

    **SQL Syntax**:
    ```sql
    CREATE TRIGGER trigger_name
    BEFORE INSERT ON table_name
    FOR EACH ROW
    BEGIN
        SQL statements;
    END;
    ```

    **Example**: Validate stock quantity before inserting a new product.
    """)

    sql_command = """
    CREATE TRIGGER BeforeInsertProduct
    BEFORE INSERT ON products
    FOR EACH ROW
    BEGIN
        IF NEW.stock < 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock cannot be negative';
        END IF;
    END;
    """
    st.code(sql_command, language="sql")

    st.markdown("### Interactive Example")
    new_product_name = st.text_input("Enter Product Name:")
    new_stock = st.number_input("Enter Stock Quantity:", step=1, value=10)
    new_price = st.number_input("Enter Price:", step=1, value=1000)

    if st.button("Insert Product with BEFORE Trigger"):
        if new_stock < 0:
            st.error("❌ BEFORE Trigger Activated: Stock cannot be negative!")
        else:
            new_row = pd.DataFrame({
                'product_id': [len(products) + 1],
                'product_name': [new_product_name],
                'stock': [new_stock],
                'price': [new_price]
            })
            products = pd.concat([products, new_row], ignore_index=True)
            st.success("✅ Product Inserted Successfully!")
        st.dataframe(products)

# AFTER Trigger
with tabs[1]:
    st.header("🔹 AFTER Trigger")
    st.markdown("""
    **Definition**: An `AFTER` trigger executes after an `INSERT`, `UPDATE`, or `DELETE` operation on a table.

    **SQL Syntax**:
    ```sql
    CREATE TRIGGER trigger_name
    AFTER INSERT ON table_name
    FOR EACH ROW
    BEGIN
        SQL statements;
    END;
    ```

    **Example**: Log an action in the `audit_log` table after inserting a new product.
    """)

    sql_command = """
    CREATE TRIGGER AfterInsertProduct
    AFTER INSERT ON products
    FOR EACH ROW
    BEGIN
        INSERT INTO audit_log (action, product_id, timestamp)
        VALUES ('INSERT', NEW.product_id, CURRENT_TIMESTAMP);
    END;
    """
    st.code(sql_command, language="sql")

    st.markdown("### Interactive Example")
    new_product_name = st.text_input("Enter Product Name (AFTER Trigger):", key="after_name")
    new_stock = st.number_input("Enter Stock Quantity:", step=1, value=10, key="after_stock")
    new_price = st.number_input("Enter Price:", step=1, value=1000, key="after_price")

    if st.button("Insert Product with AFTER Trigger"):
        new_row = pd.DataFrame({
            'product_id': [len(products) + 1],
            'product_name': [new_product_name],
            'stock': [new_stock],
            'price': [new_price]
        })
        products = pd.concat([products, new_row], ignore_index=True)
        
        log_row = pd.DataFrame({
            'action': ['INSERT'],
            'product_id': [len(products)],
            'timestamp': [pd.Timestamp.now()]
        })
        audit_log = pd.concat([audit_log, log_row], ignore_index=True)

        st.success("✅ Product Inserted and Log Updated!")
        st.markdown("**Updated Product Table:**")
        st.dataframe(products)
        st.markdown("**Updated Audit Log Table:**")
        st.dataframe(audit_log)

# INSTEAD OF Trigger
with tabs[2]:
    st.header("🔹 INSTEAD OF Trigger")
    st.markdown("""
    **Definition**: An `INSTEAD OF` trigger replaces the normal operation for a `VIEW` during an `INSERT`, `UPDATE`, or `DELETE`.

    **SQL Syntax**:
    ```sql
    CREATE TRIGGER trigger_name
    INSTEAD OF INSERT ON view_name
    FOR EACH ROW
    BEGIN
        SQL statements;
    END;
    ```

    **Example**: Insert into a base table through a view using an `INSTEAD OF` trigger.
    """)

    sql_command = """
    CREATE TRIGGER InsteadOfInsertView
    INSTEAD OF INSERT ON product_view
    FOR EACH ROW
    BEGIN
        INSERT INTO products (product_id, product_name, stock, price)
        VALUES (NEW.product_id, NEW.product_name, NEW.stock, NEW.price);
    END;
    """
    st.code(sql_command, language="sql")

# INSERT/UPDATE/DELETE
with tabs[3]:
    st.header("🔹 Triggers on INSERT, UPDATE, DELETE")
    st.markdown("""
    Triggers can be created for any of these operations:
    
    1. **INSERT**: Automatically execute actions when a row is inserted.
    2. **UPDATE**: Automatically execute actions when a row is updated.
    3. **DELETE**: Automatically execute actions when a row is deleted.

    **SQL Example for DELETE Trigger**:
    ```sql
    CREATE TRIGGER AfterDeleteProduct
    AFTER DELETE ON products
    FOR EACH ROW
    BEGIN
        INSERT INTO audit_log (action, product_id, timestamp)
        VALUES ('DELETE', OLD.product_id, CURRENT_TIMESTAMP);
    END;
    ```
    """)

# Triggering Conditions
with tabs[4]:
    st.header("🔹 Triggering Conditions (ROW vs. STATEMENT Level)")
    st.markdown("""
    **ROW-Level Trigger**: Executes once for each row affected.
    
    **STATEMENT-Level Trigger**: Executes once for the entire statement.

    **SQL Example for ROW-Level Trigger**:
    ```sql
    CREATE TRIGGER RowLevelTrigger
    AFTER INSERT ON products
    FOR EACH ROW
    BEGIN
        -- Trigger code here
    END;
    ```

    **SQL Example for STATEMENT-Level Trigger**:
    ```sql
    CREATE TRIGGER StatementLevelTrigger
    AFTER INSERT ON products
    FOR EACH STATEMENT
    BEGIN
        -- Trigger code here
    END;
    ```
    """)

# Dropping Triggers
with tabs[5]:
    st.header("🔹 Dropping Triggers")
    st.markdown("""
    If a trigger is no longer needed, it can be dropped using the `DROP TRIGGER` statement.

    **SQL Syntax**:
    ```sql
    DROP TRIGGER trigger_name;
    ```

    **Example**:
    ```sql
    DROP TRIGGER BeforeInsertProduct;
    ```
    """)

    sql_command = "DROP TRIGGER trigger_name;"
    st.code(sql_command, language="sql")

# Footer Quiz Section
st.markdown("---")
st.header("🎯 Test Your Knowledge!")
quiz_question = st.multiselect(
    "Which statements about triggers are true? (Select all that apply)",
    [
        "A BEFORE trigger executes before an operation.",
        "An AFTER trigger executes instead of an operation.",
        "INSTEAD OF triggers work with views.",
        "Triggers can be created for INSERT, UPDATE, and DELETE operations."
    ],
    key="quiz_triggers"
)

if st.button("Submit Answer", key="quiz_submit_triggers"):
    correct_answers = {
        "A BEFORE trigger executes before an operation.",
        "INSTEAD OF triggers work with views.",
        "Triggers can be created for INSERT, UPDATE, and DELETE operations."
    }
    selected_answers = set(quiz_question)

    if selected_answers == correct_answers:
        st.success("Correct! 🎉 Triggers automate database operations effectively.")
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