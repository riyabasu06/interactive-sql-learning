import streamlit as st
import pandas as pd

# Sample Data for Demonstration
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'age': [25, 35, 30, 40, 29],
    'department': ['HR', 'Engineering', 'Marketing', 'Engineering', 'HR'],
    'salary': [50000, 60000, 55000, 70000, 48000]
})

departments = pd.DataFrame({
    'dept_id': [101, 102, 103, 104],
    'department_name': ['HR', 'Engineering', 'Marketing', 'Finance'],
    'budget': [150000, 300000, 200000, 100000]
})

# Title and Introduction
st.title("🔍 Subqueries")
st.markdown("""
Welcome to the interactive SQL subqueries tutorial! 🚀

Subqueries are queries embedded within another query. They are powerful tools for performing complex filtering, aggregation, and comparisons in SQL. Let's explore each type of subquery with examples and hands-on interaction! 🎓

---

Here are the tables we will use:
""")

# Display Sample Tables
st.subheader("Employee Table")
st.dataframe(employees)

st.subheader("Department Table")
st.dataframe(departments)

# Tabs for Subtopics
tabs = st.tabs([
    "Subqueries in SELECT", "Subqueries in WHERE", "Subqueries in FROM",
    "Correlated Subqueries", "EXISTS Operator", "IN Operator"
])

# Subqueries in SELECT
with tabs[0]:
    st.header("📋 Subqueries in SELECT Statements")
    st.markdown("""
    Subqueries in the `SELECT` statement are used to calculate values dynamically.

    **Example:** Add a column showing the average salary across all employees.
    """)
    avg_salary = employees['salary'].mean()
    sql_command = f"""
    SELECT emp_id, name, salary,
           (SELECT AVG(salary) FROM employees) AS avg_salary
    FROM employees;
    """
    employees_with_avg = employees.copy()
    employees_with_avg['avg_salary'] = avg_salary
    
    st.code(sql_command, language="sql")
    st.markdown("**Result:**")
    st.dataframe(employees_with_avg)

# Subqueries in WHERE
with tabs[1]:
    st.header("🔍 Subqueries in WHERE Clause")
    st.markdown("""
    Subqueries in the `WHERE` clause filter rows based on the results of another query.

    **Example:** Find employees whose salary is above the average salary.
    """)
    filtered_employees = employees[employees['salary'] > avg_salary]
    sql_command = f"""
    SELECT emp_id, name, salary
    FROM employees
    WHERE salary > (SELECT AVG(salary) FROM employees);
    """
    
    st.code(sql_command, language="sql")
    st.markdown("**Result:**")
    st.dataframe(filtered_employees)

# Subqueries in FROM
with tabs[2]:
    st.header("📋 Subqueries in FROM Clause")
    st.markdown("""
    Subqueries in the `FROM` clause act as a derived table.

    **Example:** Calculate the total salary grouped by department using a subquery.
    """)
    grouped_salaries = employees.groupby('department')['salary'].sum().reset_index(name='Total Salary')
    sql_command = f"""
    SELECT department, Total_Salary
    FROM (SELECT department, SUM(salary) AS Total_Salary FROM employees GROUP BY department) AS derived_table; 
    """
    
    st.code(sql_command, language="sql")
    st.markdown("**Result:**")
    st.dataframe(grouped_salaries)

# Correlated Subqueries
with tabs[3]:
    st.header("🔄 Correlated Subqueries")
    st.markdown("""
    Correlated subqueries reference columns from the outer query.

    **Example:** Find employees who earn more than the average salary in their department.
    """)
    dept_avg_salary = employees.groupby('department')['salary'].transform('mean')
    correlated_result = employees[employees['salary'] > dept_avg_salary]
    sql_command = f"""
    SELECT emp_id, name, salary
    FROM employees outer
    WHERE salary > (SELECT AVG(salary) FROM employees inner WHERE inner.department = outer.department);
    """
    
    st.code(sql_command, language="sql")
    st.markdown("**Result:**")
    st.dataframe(correlated_result)

# EXISTS Operator
with tabs[4]:
    st.header("✅ EXISTS Operator")
    st.markdown("""
    The `EXISTS` operator checks whether a subquery returns any rows. If the subquery returns at least one row, the `EXISTS` condition evaluates to `TRUE`.
    
    **Example:** Find departments that have employees.
    """)
    
    sql_command_dynamic = f"""
    SELECT department_name
    FROM departments
    WHERE EXISTS (SELECT 1 FROM employees WHERE employees.department = departments.department_name);
    """
    
    st.code(sql_command_dynamic, language="sql")
    
    st.markdown("""
    **Why use `SELECT 1`?**
    - The value in the `SELECT` clause inside the subquery (e.g., `1`) is a placeholder.
    - The subquery is only used to check for existence; it doesn’t return any actual data. 
    - You can use any constant (e.g., `1`, `NULL`, or `*`), but using `1` is a common convention for readability.
""")
    # Display Result
    existing_departments = departments[departments['department_name'].isin(employees['department'])]
    st.markdown("**Result:**")
    st.dataframe(existing_departments)


# IN Operator with Subqueries
with tabs[5]:
    st.header("📋 IN Operator with Subqueries")
    st.markdown("""
    The `IN` operator checks whether a value exists in a list returned by a subquery.

    **Example:** Find employees who work in departments with a budget greater than 200,000.
    """)
    high_budget_departments = departments[departments['budget'] > 200000]['department_name']
    in_operator_result = employees[employees['department'].isin(high_budget_departments)]
    sql_command = f"""
    SELECT emp_id, name, department
    FROM employees
    WHERE department IN (SELECT department_name FROM departments WHERE budget > 200000);
    """
    
    st.code(sql_command, language="sql")
    st.markdown("**Result:**")
    st.dataframe(in_operator_result)

# Footer Quiz Section
st.markdown("---")
st.header("🎯 Test Your Knowledge!")
quiz_question = st.radio(
    "Which statement about subqueries is correct?",
    [
        "Subqueries can only be used in the WHERE clause.",
        "A subquery can return multiple columns and rows.",
        "The EXISTS operator in a subquery returns actual data from the table.",
        "Subqueries cannot be nested inside another subquery."
    ],
    key="subqueries_quiz"
)

if st.button("Submit Answer", key="subqueries_quiz_submit"):
    if quiz_question == "A subquery can return multiple columns and rows.":
        st.success("Correct! 🎉 Subqueries can return multiple columns and rows, depending on their use.")
    else:
        st.error("Oops! That’s not right. Hint: Think about the versatility of subqueries and what they can return.")

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