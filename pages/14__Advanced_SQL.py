import streamlit as st
import pandas as pd

# Title and Introduction
st.title("🔍 Advanced SQL")
st.markdown("""
Welcome to the **Advanced SQL Tutorial**! 🚀

This tutorial covers advanced SQL concepts to help you write more efficient and complex queries.

---

### Topics Covered:
1. **Common Table Expressions (CTEs)**
2. **Window Functions** (`ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, etc.)
3. **Recursive Queries**
4. **Pivoting Data**
5. **Analytical Functions**
6. **Performance Tuning and Optimization**

---

Here’s the sample data we’ll use:
""")

# Sample Data
sales = pd.DataFrame({
    'sale_id': [1, 2, 3, 4, 5],
    'product': ['Laptop', 'Phone', 'Tablet', 'Laptop', 'Phone'],
    'category': ['Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics'],
    'region': ['North', 'South', 'North', 'East', 'West'],
    'quantity': [2, 3, 1, 5, 4],
    'price': [1000, 500, 300, 1000, 500]
})
st.subheader("Sales Table")
st.dataframe(sales)

# Tabs for Subtopics
tabs = st.tabs([
    "CTEs", "Window Functions", "Recursive Queries",
    "Pivoting Data", "Analytical Functions", "Performance Tuning"
])

# Common Table Expressions (CTEs)
with tabs[0]:
    st.header("🔹 Common Table Expressions (CTEs)")
    st.markdown("""
    **Definition**: A `WITH` clause that creates a temporary result set, which can be referenced within the main SQL query.

    **SQL Syntax**:
    ```sql
    WITH cte_name AS (
        SELECT ...
    )
    SELECT ...
    FROM cte_name;
    ```

    **Example**: Calculate total revenue for each region using a CTE.
    """)

    sql_command = """
    WITH RegionRevenue AS (
        SELECT region, SUM(quantity * price) AS total_revenue
        FROM sales
        GROUP BY region
    )
    SELECT *
    FROM RegionRevenue;
    """
    st.code(sql_command, language="sql")

    st.markdown("### Example")
    region_revenue = sales.groupby('region').apply(lambda x: (x['quantity'] * x['price']).sum()).reset_index(name='total_revenue')
    st.markdown("**Region Revenue (Using CTE):**")
    st.dataframe(region_revenue)

# Window Functions
with tabs[1]:
    st.header("🔹 Window Functions")
    st.markdown("""
    **Definition**: Perform calculations across rows related to the current row within a partition.

    **Functions**:
    - `ROW_NUMBER()`: Assigns a unique number to each row within a partition.
    - `RANK()`: Ranks rows with gaps for duplicates.
    - `DENSE_RANK()`: Ranks rows without gaps for duplicates.

    **SQL Syntax**:
    ```sql
    SELECT column, ROW_NUMBER() OVER (PARTITION BY column ORDER BY column) AS row_num
    FROM table;
    ```

    **Example**: Rank sales by quantity for each region.
    """)

    sql_command = """
    SELECT sale_id, region, product, quantity,
           ROW_NUMBER() OVER (PARTITION BY region ORDER BY quantity DESC) AS row_number,
           RANK() OVER (PARTITION BY region ORDER BY quantity DESC) AS rank,
           DENSE_RANK() OVER (PARTITION BY region ORDER BY quantity DESC) AS dense_rank
    FROM sales;
    """
    st.code(sql_command, language="sql")

    st.markdown("### Example")
    sales['row_number'] = sales.groupby('region')['quantity'].rank(method='first', ascending=False).astype(int)
    sales['rank'] = sales.groupby('region')['quantity'].rank(method='min', ascending=False).astype(int)
    sales['dense_rank'] = sales.groupby('region')['quantity'].rank(method='dense', ascending=False).astype(int)
    st.dataframe(sales[['sale_id', 'region', 'product', 'quantity', 'row_number', 'rank', 'dense_rank']])

# Recursive Queries
with tabs[2]:
    st.header("🔹 Recursive Queries")
    st.markdown("""
    **Definition**: A recursive CTE is used to repeatedly execute a query until a specified condition is met.

    **SQL Syntax**:
    ```sql
    WITH RECURSIVE cte_name AS (
        SELECT ...
        UNION ALL
        SELECT ...
        FROM cte_name
        WHERE condition
    )
    SELECT ...
    FROM cte_name;
    ```

    **Example**: Generate a sequence of numbers up to 10.
    """)

    sql_command = """
    WITH RECURSIVE Numbers AS (
        SELECT 1 AS num
        UNION ALL
        SELECT num + 1
        FROM Numbers
        WHERE num < 10
    )
    SELECT *
    FROM Numbers;
    """
    st.code(sql_command, language="sql")

    st.markdown("### Example")
    numbers = pd.DataFrame({'num': list(range(1, 11))})
    st.dataframe(numbers)

# Pivoting Data
with tabs[3]:
    st.header("🔹 Pivoting Data")
    st.markdown("""
    **Definition**: Transform rows into columns to summarize data in a tabular format.

    **SQL Syntax** (Using CASE):
    ```sql
    SELECT
        region,
        SUM(CASE WHEN product = 'Laptop' THEN quantity ELSE 0 END) AS laptop_sales,
        SUM(CASE WHEN product = 'Phone' THEN quantity ELSE 0 END) AS phone_sales
    FROM sales
    GROUP BY region;
    ```

    **Example**: Pivot sales data by product.
    """)

    sql_command = """
    SELECT
        region,
        SUM(CASE WHEN product = 'Laptop' THEN quantity ELSE 0 END) AS laptop_sales,
        SUM(CASE WHEN product = 'Phone' THEN quantity ELSE 0 END) AS phone_sales
    FROM sales
    GROUP BY region;
    """
    st.code(sql_command, language="sql")

    st.markdown("### Example")
    pivot_data = sales.pivot_table(index='region', columns='product', values='quantity', aggfunc='sum', fill_value=0)
    st.dataframe(pivot_data)

# Analytical Functions
with tabs[4]:
    st.header("🔹 Analytical Functions")
    st.markdown("""
    **Definition**: Analytical functions compute values over a group of rows and return multiple rows for each group.

    **Examples**:
    - `AVG() OVER`: Calculate a moving average.
    - `SUM() OVER`: Calculate cumulative sums.
    - `LAG()`, `LEAD()`: Access previous or next row values.

    **SQL Syntax**:
    ```sql
    SELECT column, SUM(column) OVER (PARTITION BY column ORDER BY column ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)
    FROM table;
    ```

    **Example**: Calculate cumulative sales by region.
    """)

    sql_command = """
    SELECT sale_id, region, product, quantity,
           SUM(quantity) OVER (PARTITION BY region ORDER BY sale_id) AS cumulative_quantity
    FROM sales;
    """
    st.code(sql_command, language="sql")

    sales['cumulative_quantity'] = sales.groupby('region')['quantity'].cumsum()
    st.dataframe(sales[['sale_id', 'region', 'product', 'quantity', 'cumulative_quantity']])

# Performance Tuning
with tabs[5]:
    st.header("🔹 Performance Tuning and Optimization")
    st.markdown("""
    **Techniques**:
    1. Use appropriate indexes to speed up queries.
    2. Avoid `SELECT *`; select only necessary columns.
    3. Optimize joins and subqueries.
    4. Use partitions for large datasets.
    5. Analyze and rewrite queries for efficiency.

    **Example**: Create an index for the `region` column.
    """)

    sql_command = """
    CREATE INDEX idx_region ON sales(region);
    """
    st.code(sql_command, language="sql")

    st.markdown("### Tips:")
    st.markdown("""
    - Use **EXPLAIN** to analyze query execution plans.
    - Avoid functions in `WHERE` clauses that prevent index usage.
    """)

# Footer Quiz Section
st.markdown("---")
st.header("🎯 Test Your Knowledge!")
quiz_question = st.multiselect(
    "Which of the following statements about advanced SQL concepts are true? (Select all that apply)",
    [
        "CTEs simplify complex queries.",
        "Window functions calculate values across rows.",
        "Recursive queries cannot generate sequences.",
        "Pivoting transforms rows into columns."
    ],
    key="quiz_advanced_sql"
)

if st.button("Submit Answer", key="quiz_submit_advanced_sql"):
    correct_answers = {
        "CTEs simplify complex queries.",
        "Window functions calculate values across rows.",
        "Pivoting transforms rows into columns."
    }
    selected_answers = set(quiz_question)

    if selected_answers == correct_answers:
        st.success("Correct! 🎉 You’ve mastered advanced SQL concepts.")
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