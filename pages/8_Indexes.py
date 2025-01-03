import streamlit as st
import pandas as pd

# Title and Introduction
st.title("📊 Indexes")
st.markdown("""
Welcome to the interactive SQL Indexes tutorial! 🚀

**Indexes** are used to speed up data retrieval in SQL by creating an efficient lookup structure. They are crucial for database performance optimization and query execution.

---

### What We'll Cover:
1. Creating indexes
2. Types of indexes (Unique, Full-text, Composite, etc.)
3. Index performance considerations
4. DROP INDEX
5. Index optimization

---

Here’s a sample table to demonstrate indexes:
""")

# Sample Table
data = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'department': ['HR', 'Engineering', 'Marketing', 'Engineering', 'HR'],
    'salary': [50000, 60000, 55000, 70000, 48000]
})
st.subheader("Employee Table")
st.dataframe(data)

# Tabs for Subtopics
tabs = st.tabs([
    "Creating Indexes", "Types of Indexes", "Index Performance", "DROP INDEX", "Index Optimization"
])

# Creating Indexes
with tabs[0]:
    st.header("🔑 Creating Indexes")
    st.markdown("""
    Creating an index on a table column significantly improves query performance by allowing the database to locate rows more quickly.

    **SQL Syntax:**
    ```sql
    CREATE INDEX index_name ON table_name(column_name);
    ```
    **Example:** Create an index on the `department` column of the `employees` table.
    """)
    sql_command = """
    CREATE INDEX idx_department ON employees(department);
    """
    st.code(sql_command, language="sql")
    st.markdown("### Interactive Example")
    st.markdown("Run a query to filter employees by department and observe the benefits of indexing.")

    filter_department = st.selectbox("Select a department to filter:", data['department'].unique())
    filtered_data = data[data['department'] == filter_department]

    # Display the SELECT query
    select_query = f"""
    SELECT * 
    FROM employees
    WHERE department = '{filter_department}';
    """
    st.code(select_query, language="sql")

    st.markdown(f"**Filtered Results for `{filter_department}` Department:**")
    st.dataframe(filtered_data)

# Types of Indexes
with tabs[1]:
    st.header("📂 Types of Indexes")
    st.markdown("""
    SQL supports several types of indexes, each serving a specific purpose:

    1. **Unique Index**: Ensures that all values in the indexed column are unique.
    2. **Full-text Index**: Used for searching text-based data efficiently.
    3. **Composite Index**: Combines multiple columns into a single index for complex queries.

    """)

    st.markdown("### Interactive Example")
    index_type = st.radio("Choose an index type to explore:", ["Unique", "Full-text", "Composite"])
    if index_type == "Unique":
        st.code("CREATE UNIQUE INDEX idx_unique_name ON employees(name);", language="sql")
        st.markdown("**Description:** Ensures no duplicate names in the `name` column.")
    elif index_type == "Full-text":
        st.code("CREATE FULLTEXT INDEX idx_fulltext_name ON employees(name);", language="sql")
        st.markdown("**Description:** Speeds up text searches on the `name` column.")
    elif index_type == "Composite":
        st.code("CREATE INDEX idx_composite_department_salary ON employees(department, salary);", language="sql")
        st.markdown("**Description:** Optimizes queries involving both `department` and `salary` columns.")

# Index Performance
with tabs[2]:
    st.header("⚡ Index Performance Considerations")
    st.markdown("""
    While indexes improve query performance, they come with trade-offs:

    - **Advantages**:
      - Faster SELECT queries.
      - Efficient filtering and sorting.
    - **Disadvantages**:
      - Slower INSERT, UPDATE, and DELETE operations due to index maintenance.
      - Increased storage requirements.

    **Best Practices:**
    - Use indexes on frequently queried columns.
    - Avoid over-indexing to minimize performance overhead.
    """)

    st.markdown("### Example Query Performance")
    st.markdown("Imagine filtering employees by `salary`. Indexing this column can reduce query time.")
    st.code("""
    CREATE INDEX idx_salary ON employees(salary);
    SELECT * FROM employees WHERE salary > 55000;
    """, language="sql")

# DROP INDEX
with tabs[3]:
    st.header("❌ DROP INDEX")
    st.markdown("""
    If an index is no longer needed, you can drop it to save storage and improve write performance.

    **SQL Syntax:**
    ```sql
    DROP INDEX index_name ON table_name;
    ```
    **Example:** Drop the `idx_department` index.
    """)
    sql_command = """
    DROP INDEX idx_department ON employees;
    """
    st.code(sql_command, language="sql")
    st.markdown("In this example, the `idx_department` index is dropped, making queries slower.")

# Index Optimization
with tabs[4]:
    st.header("📈 Index Optimization")
    st.markdown("""
    Optimize indexes by following these guidelines:
    1. Remove unused indexes.
    2. Use composite indexes for multi-column filtering.
    3. Regularly monitor index usage statistics.

    **SQL Syntax:**
    ```sql
    ANALYZE TABLE employees;
    OPTIMIZE TABLE employees;
    ```
    """)


# Footer Quiz Section
st.markdown("---")
st.header("🎯 Test Your Knowledge!")
quiz_question = st.multiselect(
    "Which statements about SQL indexes are true? (Select all that apply)",
    [
        "Indexes improve SELECT query performance.",
        "Indexes always improve INSERT performance.",
        "Full-text indexes are used for text search.",
        "Unique indexes allow duplicate values."
    ],
    key="indexes_quiz"
)

if st.button("Submit Answer", key="indexes_quiz_submit"):
    correct_answers = {
        "Indexes improve SELECT query performance.",
        "Full-text indexes are used for text search."
    }
    selected_answers = set(quiz_question)
    if selected_answers == correct_answers:
        st.success("Correct! 🎉 Indexes improve SELECT performance and Full-text indexes are for text search.")
    else:
        missing_answers = correct_answers - selected_answers
        extra_answers = selected_answers - correct_answers
        feedback = "Oops! Here's what you got wrong:\n"
        if missing_answers:
            feedback += f"- Missing correct answer(s): {', '.join(missing_answers)}\n"
        if extra_answers:
            feedback += f"- Incorrect answer(s): {', '.join(extra_answers)}\n"
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