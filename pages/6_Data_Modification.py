import streamlit as st
import pandas as pd

# Sample Data for Demonstration
employees = pd.DataFrame({
    'emp_id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'department': ['HR', 'Engineering', 'Marketing'],
    'salary': [50000, 60000, 55000]
})

# Title and Introduction
st.title("🔧 Data Modification")
st.markdown("""
Welcome to the interactive SQL Data Modification tutorial! 🚀

Data modification statements allow you to manage and update data in your database tables. 
The four key operations are:
- `INSERT INTO`: Add new rows to a table.
- `UPDATE`: Modify existing rows in a table.
- `DELETE`: Remove rows from a table.
- `MERGE` (or `UPSERT`): Insert new rows or update existing rows based on conditions.

---

Here’s the initial sample table we'll work with:
""")

# Display Sample Table
st.subheader("Employee Table")
st.dataframe(employees)

# Tabs for Subtopics
tabs = st.tabs(["INSERT INTO", "UPDATE", "DELETE", "MERGE (UPSERT)"])

# INSERT INTO
with tabs[0]:
    st.header("➕ INSERT INTO")
    st.markdown("""
    The `INSERT INTO` statement adds new rows to a table. 

    **SQL Syntax:**
    ```sql
    INSERT INTO table_name (column1, column2, ...)
    VALUES (value1, value2, ...);
    ```

    **Example:** Add a new employee to the `employees` table.
    """)
    
    # Interactive Input
    st.markdown("### Add a New Employee")
    new_emp_id = st.number_input("Employee ID:", min_value=1, step=1, key="insert_emp_id")
    new_name = st.text_input("Employee Name:", key="insert_name")
    new_department = st.text_input("Department:", key="insert_department")
    new_salary = st.number_input("Salary:", min_value=1, step=1, key="insert_salary")
    
    # Update Table Dynamically
    if st.button("Insert Row", key="insert_row"):
        new_row = pd.DataFrame({
            'emp_id': [new_emp_id],
            'name': [new_name],
            'department': [new_department],
            'salary': [new_salary]
        })
        employees = pd.concat([employees, new_row], ignore_index=True)
        st.success("New employee added!")
    
    # Display Updated Table
    st.markdown("**Updated Employee Table:**")
    st.dataframe(employees)

    # Display SQL Command
    sql_command = f"""
    INSERT INTO employees (emp_id, name, department, salary)
    VALUES ({new_emp_id}, '{new_name}', '{new_department}', {new_salary});
    """
    st.code(sql_command, language="sql")

# UPDATE
with tabs[1]:
    st.header("✏️ UPDATE")
    st.markdown("""
    The `UPDATE` statement modifies existing rows in a table.

    **SQL Syntax:**
    ```sql
    UPDATE table_name
    SET column1 = value1, column2 = value2, ...
    WHERE condition;
    ```

    **Example:** Update an employee's salary in the `employees` table.
    """)
    
    # Interactive Input
    st.markdown("### Update Employee Salary")
    update_emp_id = st.selectbox("Choose an Employee ID to Update:", employees['emp_id'])
    new_salary = st.number_input("New Salary:", min_value=1, step=1, key="update_salary")
    
    # Update Table Dynamically
    if st.button("Update Salary", key="update_salary_button"):
        employees.loc[employees['emp_id'] == update_emp_id, 'salary'] = new_salary
        st.success("Employee salary updated!")
    
    # Display Updated Table
    st.markdown("**Updated Employee Table:**")
    st.dataframe(employees)

    # Display SQL Command
    sql_command = f"""
    UPDATE employees
    SET salary = {new_salary}
    WHERE emp_id = {update_emp_id};
    """
    
    st.code(sql_command, language="sql")

# DELETE
with tabs[2]:
    st.header("🗑️ DELETE")
    st.markdown("""
    The `DELETE` statement removes rows from a table.

    **SQL Syntax:**
    ```sql
    DELETE FROM table_name
    WHERE condition;
    ```

    **Example:** Delete an employee from the `employees` table.
    """)
    
    # Interactive Input
    st.markdown("### Delete an Employee")
    delete_emp_id = st.selectbox("Choose an Employee ID to Delete:", employees['emp_id'])
    
    # Delete Row Dynamically
    if st.button("Delete Employee", key="delete_employee"):
        employees = employees[employees['emp_id'] != delete_emp_id]
        st.success("Employee deleted!")
    
    # Display Updated Table
    st.markdown("**Updated Employee Table:**")
    st.dataframe(employees)

    # Display SQL Command
    sql_command = f"""
    DELETE FROM employees
    WHERE emp_id = {delete_emp_id};
    """
    
    st.code(sql_command, language="sql")

# MERGE (UPSERT)
with tabs[3]:
    st.header("🔀 MERGE (UPSERT)")
    st.markdown("""
    The `MERGE` statement inserts new rows or updates existing rows based on a condition. 
    It is also known as `UPSERT` in some databases.

    **SQL Syntax:**
    ```sql
    MERGE INTO table_name AS target
    USING source_table AS source
    ON condition
    WHEN MATCHED THEN
        UPDATE SET column1 = value1, column2 = value2, ...
    WHEN NOT MATCHED THEN
        INSERT (column1, column2, ...) VALUES (value1, value2, ...);
    ```

    **Example:** Insert a new employee or update their salary if they already exist.
    """)
    
    # Interactive Input
    st.markdown("### Merge (Upsert) Employee")
    merge_emp_id = st.number_input("Employee ID:", min_value=1, step=1, key="merge_emp_id")
    merge_name = st.text_input("Employee Name:", key="merge_name")
    merge_department = st.text_input("Department:", key="merge_department")
    merge_salary = st.number_input("Salary:", min_value=1, step=1, key="merge_salary")
    
    # Merge Logic
    if st.button("Merge Employee", key="merge_employee"):
        if merge_emp_id in employees['emp_id'].values:
            employees.loc[employees['emp_id'] == merge_emp_id, ['name', 'department', 'salary']] = [merge_name, merge_department, merge_salary]
            st.success("Employee record updated!")
        else:
            new_row = pd.DataFrame({
                'emp_id': [merge_emp_id],
                'name': [merge_name],
                'department': [merge_department],
                'salary': [merge_salary]
            })
            employees = pd.concat([employees, new_row], ignore_index=True)
            st.success("New employee record inserted!")
    
    # Display Updated Table
    st.markdown("**Updated Employee Table:**")
    st.dataframe(employees)

    # Display SQL Command
    sql_command = f"""
    MERGE INTO employees AS target
    USING (SELECT {merge_emp_id} AS emp_id, '{merge_name}' AS name, '{merge_department}' AS department, {merge_salary} AS salary) AS source
    ON target.emp_id = source.emp_id
    WHEN MATCHED THEN
        UPDATE SET name = '{merge_name}', department = '{merge_department}', salary = {merge_salary}
    WHEN NOT MATCHED THEN
        INSERT (emp_id, name, department, salary)
        VALUES ({merge_emp_id}, '{merge_name}', '{merge_department}', {merge_salary});
    """
    
    st.code(sql_command, language="sql")

# Footer Quiz Section
st.markdown("---")
st.header("🎯 Test Your Knowledge!")
quiz_question = st.radio(
    "Which SQL statement is used to update existing rows or insert new rows if they don’t exist?",
    ["INSERT INTO", "UPDATE", "DELETE", "MERGE (UPSERT)"],
    key="data_modification_quiz"
)
if st.button("Submit Answer", key="data_modification_quiz_submit"):
    if quiz_question == "MERGE (UPSERT)":
        st.success("Correct! 🎉 The MERGE statement is used to perform an UPSERT operation.")
    else:
        st.error("Oops! Try again. Hint: It combines INSERT and UPDATE operations.")

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