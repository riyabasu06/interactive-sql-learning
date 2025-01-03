import streamlit as st
import pandas as pd

# Sample data for demonstration
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'dept_id': [101, 102, 103, 101, 102],
    'manager_id': [None, 1, 1, 2, 3] 
})

departments = pd.DataFrame({
    'dept_id': [101, 102, 103, 104],
    'department_name': ['HR', 'Engineering', 'Marketing', 'Finance']
})

salaries = pd.DataFrame({
    'emp_id': [1, 2, 3, 6],
    'salary': [50000, 60000, 55000, 70000]
})

# Title and Introduction
st.title("🧠 SQL Joins🎉")
st.markdown("""
Welcome to the interactive SQL Joins tutorial! 🚀 

SQL joins allow you to combine rows from two or more tables based on a related column. 
Let's explore each type of join with examples and hands-on interaction! 🎓

---
""")

# Tabs for subtopics
tabs = st.tabs([
    "INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN", "CROSS JOIN", "SELF JOIN", "NATURAL JOIN"
])

# Helper function to display tables
def display_tables():
    st.subheader("Employee Table")
    st.dataframe(employees)
    st.subheader("Department Table")
    st.dataframe(departments)
    st.subheader("Salary Table")
    st.dataframe(salaries)

# INNER JOIN
with tabs[0]:
    st.header("🔗 INNER JOIN")
    st.markdown("""
    The `INNER JOIN` returns only the rows where there is a match in both tables.

    **SQL Syntax:**
    ```sql
    SELECT e.emp_id, e.name, d.department_name
    FROM employees e
    INNER JOIN departments d
    ON e.dept_id = d.dept_id;
    ```
    """)
    display_tables()
    st.subheader("Result:")
    inner_join_result = pd.merge(employees, departments, on='dept_id', how='inner')
    st.dataframe(inner_join_result)

# LEFT JOIN
with tabs[1]:
    st.header("🔗 LEFT JOIN")
    st.markdown("""
    The `LEFT JOIN` returns all rows from the left table and the matching rows from the right table. 
    If there is no match, NULL values are returned for the right table's columns.

    **SQL Syntax:**
    ```sql
    SELECT e.emp_id, e.name, d.department_name
    FROM employees e
    LEFT JOIN departments d
    ON e.dept_id = d.dept_id;
    ```
    """)
    display_tables()
    st.subheader("Result:")
    left_join_result = pd.merge(employees, departments, on='dept_id', how='left')
    st.dataframe(left_join_result)

# RIGHT JOIN
with tabs[2]:
    st.header("🔗 RIGHT JOIN")
    st.markdown("""
    The `RIGHT JOIN` returns all rows from the right table and the matching rows from the left table. 
    If there is no match, NULL values are returned for the left table's columns.

    **SQL Syntax:**
    ```sql
    SELECT e.emp_id, e.name, d.department_name
    FROM employees e
    RIGHT JOIN departments d
    ON e.dept_id = d.dept_id;
    ```
    """)
    display_tables()
    st.subheader("Result:")
    right_join_result = pd.merge(employees, departments, on='dept_id', how='right')
    st.dataframe(right_join_result)

# FULL JOIN
with tabs[3]:
    st.header("🔗 FULL JOIN")
    st.markdown("""
    The `FULL JOIN` returns all rows when there is a match in either the left or right table. 
    Non-matching rows will have NULLs for the missing data.

    **SQL Syntax:**
    ```sql
    SELECT e.emp_id, e.name, d.department_name
    FROM employees e
    FULL OUTER JOIN departments d
    ON e.dept_id = d.dept_id;
    ```
    """)
    display_tables()
    st.subheader("Result:")
    full_join_result = pd.merge(employees, departments, on='dept_id', how='outer')
    st.dataframe(full_join_result)

# CROSS JOIN
with tabs[4]:
    st.header("🔗 CROSS JOIN")
    st.markdown("""
    The `CROSS JOIN` returns the Cartesian product of both tables (i.e., every combination of rows from the two tables).

    **SQL Syntax:**
    ```sql
    SELECT e.name, d.department_name
    FROM employees e
    CROSS JOIN departments d;
    ```
    """)
    display_tables()
    st.subheader("Result:")
    cross_join_result = employees.assign(key=1).merge(departments.assign(key=1), on='key').drop('key', axis=1)
    st.dataframe(cross_join_result)

# SELF JOIN
with tabs[5]:
    st.header("🔗 SELF JOIN")
    st.markdown("""
    A `Self Join` is a join of a table with itself. It is often used to find hierarchical or relational data within the same table.

    **SQL Syntax:**
    ```sql
    SELECT e1.name AS Employee, e2.name AS Manager
    FROM employees e1
    INNER JOIN employees e2
    ON e1.manager_id = e2.emp_id;
    ```

    In this example, we find the manager of each employee using the `manager_id` column.
    """)
    
    # Display the Employee Table
    st.subheader("Employee Table")
    st.dataframe(employees)
    
    # Perform Self Join
    self_join_result = pd.merge(
        employees,  # Table e1
        employees,  # Table e2
        left_on='manager_id',
        right_on='emp_id',
        suffixes=('_employee', '_manager')
    )
    
    # Select relevant columns for display
    self_join_result = self_join_result[['name_employee', 'name_manager']]
    self_join_result.columns = ['Employee', 'Manager']
    
    # Display Self Join Result
    st.subheader("Result of Self Join")
    st.dataframe(self_join_result)

# NATURAL JOIN
with tabs[6]:
    st.header("🔗 NATURAL JOIN")
    st.markdown("""
    The `NATURAL JOIN` automatically joins tables based on all columns with the same name and data type. 
    It avoids explicitly specifying the join condition.

    **SQL Syntax:**
    ```sql
    SELECT *
    FROM employees
    NATURAL JOIN departments;
    ```
    """)
    display_tables()
    st.subheader("Result:")
    natural_join_result = pd.merge(employees, departments, on='dept_id')  # Same as INNER JOIN for this data
    st.dataframe(natural_join_result)

# Footer Quiz
st.markdown("---")
st.header("🎯 Test Your Knowledge!")
quiz_question = st.radio(
    "Which join returns all rows from both tables, even when there are no matches?",
    ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"]
)
if st.button("Submit Answer"):
    if quiz_question == "FULL JOIN":
        st.success("Correct! 🎉 The FULL JOIN includes all rows from both tables, filling unmatched fields with NULLs.")
    else:
        st.error("Oops! Try again. Hint: It's the one that combines everything. 😉")

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
