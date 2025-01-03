import streamlit as st
import pandas as pd

# Title and Introduction
st.title("🔍 Views")
st.markdown("""
Welcome to the interactive SQL Views tutorial! 🚀

A **view** is a virtual table that provides a way to simplify complex queries, improve data security, and organize data presentation.

---

### What We'll Cover:
1. Creating Views
2. Updating Views
3. Materialized Views
4. Advantages and Disadvantages of Views
5. Dropping Views

---

Here’s the sample data we’ll work with:
""")

# Sample Data
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'department': ['HR', 'Engineering', 'Marketing', 'Engineering'],
    'salary': [50000, 60000, 55000, 70000]
})

departments = pd.DataFrame({
    'dept_id': [101, 102, 103],
    'department_name': ['HR', 'Engineering', 'Marketing'],
    'manager': ['Eve', 'Tom', 'Susan']
})

st.subheader("Employee Table")
st.dataframe(employees)

st.subheader("Department Table")
st.dataframe(departments)

# Tabs for Subtopics
tabs = st.tabs([
    "Creating Views", "Updating Views", "Materialized Views",
    "Advantages & Disadvantages", "Dropping Views"
])

# Creating Views
with tabs[0]:
    st.header("🔧 Creating Views")
    st.markdown("""
    **Definition**: A view is a saved query that acts as a virtual table. It doesn't store data but retrieves it dynamically from underlying tables.

    **SQL Syntax**:
    ```sql
    CREATE VIEW view_name AS
    SELECT column1, column2, ...
    FROM table_name
    WHERE condition;
    ```

    **Example**: Create a view to display employees from the Engineering department.
    """)

    sql_command = """
    CREATE VIEW engineering_employees AS
    SELECT emp_id, name, salary
    FROM employees
    WHERE department = 'Engineering';
    """
    st.code(sql_command, language="sql")

    st.markdown("### Interactive Example")
    filter_department = st.selectbox("Select a department to create a view:", employees['department'].unique())
    view_data = employees[employees['department'] == filter_department]
    st.markdown(f"**View for `{filter_department}` Department:**")
    st.dataframe(view_data)

# Updating Views
with tabs[1]:
    st.header("✏️ Updating Views")
    st.markdown("""
    **Can Views Be Updated?**
    - Yes, if they are simple and based on a single table without aggregate functions.
    - No, if they involve joins, groupings, or computed columns.

    **SQL Syntax**:
    ```sql
    CREATE OR REPLACE VIEW view_name AS
    SELECT column1, column2, ...
    FROM table_name
    WHERE condition;
    ```

    **Example**: Update the `engineering_employees` view to include employee IDs greater than 1.
    """)

    sql_command = """
    CREATE OR REPLACE VIEW engineering_employees AS
    SELECT emp_id, name, salary
    FROM employees
    WHERE department = 'Engineering' AND emp_id > 1;
    """
    st.code(sql_command, language="sql")

    st.markdown("### Interactive Example")
    min_emp_id = st.number_input("Set a minimum Employee ID for the view:", min_value=1, value=1)
    updated_view_data = employees[(employees['department'] == 'Engineering') & (employees['emp_id'] > min_emp_id)]
    st.markdown(f"**Updated View for Employee IDs > {min_emp_id}:**")
    st.dataframe(updated_view_data)

# Materialized Views
with tabs[2]:
    st.header("📂 Materialized Views")
    st.markdown("""
    **Definition**: A materialized view stores the result of a query as a physical table, unlike a regular view, which is virtual.

    **SQL Syntax**:
    ```sql
    CREATE MATERIALIZED VIEW view_name AS
    SELECT column1, column2, ...
    FROM table_name
    WHERE condition;
    ```

    **Example**: Create a materialized view for employees with a salary greater than 60,000.
    """)

    sql_command = """
    CREATE MATERIALIZED VIEW high_salary_employees AS
    SELECT emp_id, name, department, salary
    FROM employees
    WHERE salary > 60000;
    """
    st.code(sql_command, language="sql")

    high_salary_data = employees[employees['salary'] > 60000]
    st.markdown("**Materialized View:** Employees with Salary > 60,000")
    st.dataframe(high_salary_data)

# Advantages & Disadvantages
with tabs[3]:
    st.header("⚖️ Advantages & Disadvantages")
    st.markdown("""
    **Advantages of Views**:
    1. Simplifies complex queries by abstracting them.
    2. Enhances security by restricting direct access to underlying tables.
    3. Provides consistent and reusable query results.

    **Disadvantages of Views**:
    1. Can slow performance for large datasets (since views are dynamically computed).
    2. Limited support for updating views with complex logic.
    3. Materialized views require extra storage and maintenance.

    **Interactive Comparison**:
    - Views are better for dynamic data presentation.
    - Materialized views are better for performance-critical queries.
    """)

# Dropping Views
with tabs[4]:
    st.header("❌ Dropping Views")
    st.markdown("""
    If a view is no longer needed, you can drop it using the `DROP VIEW` statement.

    **SQL Syntax**:
    ```sql
    DROP VIEW view_name;
    ```

    **Example**: Drop the `engineering_employees` view.
    """)

    sql_command = """
    DROP VIEW engineering_employees;
    """
    st.code(sql_command, language="sql")

    

# Footer Quiz Section
st.markdown("---")
st.header("🎯 Test Your Knowledge!")
quiz_question = st.multiselect(
    "Which of the following statements about views are true? (Select all that apply)",
    [
        "A view is a virtual table.",
        "Materialized views store data physically.",
        "Views always improve query performance.",
        "Views can enhance security."
    ],
    key="views_quiz"
)

if st.button("Submit Answer", key="quiz_submit_views"):
    correct_answers = {"A view is a virtual table.", "Materialized views store data physically.", "Views can enhance security."}
    selected_answers = set(quiz_question)
    
    if selected_answers == correct_answers:
        st.success("Correct! 🎉 Views are virtual, materialized views are physical, and views enhance security.")
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