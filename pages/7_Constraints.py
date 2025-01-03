import streamlit as st
import pandas as pd

# Title and Introduction
st.title("🔒 Constraints")
st.markdown("""
Welcome to the interactive SQL Constraints tutorial! 🚀

**Constraints** are rules enforced on table columns to ensure data integrity and accuracy. The six major constraints are:
- `PRIMARY KEY`: Uniquely identifies each row in a table.
- `FOREIGN KEY`: Links rows in one table to rows in another table.
- `UNIQUE`: Ensures all values in a column are unique.
- `CHECK`: Ensures values in a column meet a specific condition.
- `NOT NULL`: Ensures a column cannot have a `NULL` value.
- `DEFAULT`: Assigns a default value to a column when no value is provided.

---

Here’s the initial sample table to work with:
""")

# Initial Sample Tables
employees = pd.DataFrame({
    'emp_id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'department': ['HR', 'Engineering', 'Marketing'],
    'salary': [50000, 60000, 55000]
})
departments = pd.DataFrame({
    'dept_id': [101, 102, 103],
    'department_name': ['HR', 'Engineering', 'Marketing']
})

st.subheader("Employee Table")
st.dataframe(employees)

st.subheader("Department Table")
st.dataframe(departments)

# Tabs for Subtopics
tabs = st.tabs(["PRIMARY KEY", "FOREIGN KEY", "UNIQUE", "CHECK", "NOT NULL", "DEFAULT"])

# PRIMARY KEY
with tabs[0]:
    st.header("🔑 PRIMARY KEY Constraint")
    st.markdown("""
    The `PRIMARY KEY` constraint uniquely identifies each row in a table. 
    A table can have only one primary key, and it must consist of columns with unique and non-null values.
    """)
    
    # SQL Query
    sql_command = """
    CREATE TABLE employees (
        emp_id INT PRIMARY KEY,
        name VARCHAR(50),
        department VARCHAR(50),
        salary DECIMAL(10, 2)
    );
    """
    st.code(sql_command, language="sql")
    
    # Add new row and check for duplicate emp_id
    st.markdown("### Add New Employee")
    new_emp_id = st.number_input("Employee ID (Primary Key):", min_value=1, step=1)
    new_name = st.text_input("Name:")
    new_department = st.text_input("Department:")
    new_salary = st.number_input("Salary:", min_value=1, step=1)
    
    if st.button("Add Row", key="primary_key"):
        new_row = pd.DataFrame({
            'emp_id': [new_emp_id],
            'name': [new_name],
            'department': [new_department],
            'salary': [new_salary]
        })
        if new_emp_id in employees['emp_id'].values:
            st.error("❌ Duplicate Employee ID! The PRIMARY KEY constraint is violated.")
        else:
            employees = pd.concat([employees, new_row], ignore_index=True)
            st.success("✅ Row added successfully! PRIMARY KEY constraint maintained.")
        st.dataframe(employees)

# FOREIGN KEY
with tabs[1]:
    st.header("🔗 FOREIGN KEY Constraint")
    st.markdown("""
    The `FOREIGN KEY` constraint links a column in one table to the primary key column in another table. 
    A foreign key column can be `NULL`, which indicates no relationship for that row.
    """)
    
    # SQL Query
    sql_command = """
    CREATE TABLE employees (
        emp_id INT PRIMARY KEY,
        name VARCHAR(50),
        department VARCHAR(50),
        salary DECIMAL(10, 2),
        FOREIGN KEY (department) REFERENCES departments(department_name)
    );
    """
    st.code(sql_command, language="sql")

    st.markdown("### Add New Employee with Department")
    new_emp_id = st.number_input("Employee ID:", min_value=1, step=1, key="foreign_emp_id")
    new_name = st.text_input("Name:", key="foreign_name")
    new_department = st.text_input("Department (Foreign Key):", key="foreign_department")
    new_salary = st.number_input("Salary:", min_value=1, step=1, key="foreign_salary")
    
    if st.button("Add Row", key="foreign_key"):
        new_department = new_department if new_department.strip() else None
        
        new_row = pd.DataFrame({
            'emp_id': [new_emp_id],
            'name': [new_name],
            'department': [new_department],
            'salary': [new_salary]
        })

        if new_department is not None and new_department not in departments['department_name'].values:
            st.error(f"❌ Department '{new_department}' does not exist in Departments table. FOREIGN KEY constraint violated.")
        else:
            employees = pd.concat([employees, new_row], ignore_index=True)
            st.success("✅ Row added successfully! FOREIGN KEY constraint maintained.")
        st.dataframe(employees)

# UNIQUE
with tabs[2]:
    st.header("🌟 UNIQUE Constraint")
    st.markdown("""
    The `UNIQUE` constraint ensures all values in a column are unique, allowing no duplicates.
    """)
    
    # SQL Query
    sql_command = """
    CREATE TABLE employees (
        emp_id INT PRIMARY KEY,
        name VARCHAR(50) UNIQUE,
        department VARCHAR(50),
        salary DECIMAL(10, 2)
    );
    """
    st.code(sql_command, language="sql")
    
    st.markdown("### Add New Employee with Unique Name")
    new_emp_id = st.number_input("Employee ID:", min_value=1, step=1, key="unique_emp_id")
    new_name = st.text_input("Name (Unique):", key="unique_name")
    new_department = st.text_input("Department:", key="unique_department")
    new_salary = st.number_input("Salary:", min_value=1, step=1, key="unique_salary")
    
    if st.button("Add Row", key="unique_key"):
        new_row = pd.DataFrame({
            'emp_id': [new_emp_id],
            'name': [new_name],
            'department': [new_department],
            'salary': [new_salary]
        })
        if new_name in employees['name'].values:
            st.error(f"❌ Employee name '{new_name}' already exists. UNIQUE constraint violated.")
        else:
            employees = pd.concat([employees, new_row], ignore_index=True)
            st.success("✅ Row added successfully! UNIQUE constraint maintained.")
        st.dataframe(employees)

# CHECK
with tabs[3]:
    st.header("✅ CHECK Constraint")
    st.markdown("""
    The `CHECK` constraint ensures values in a column meet a specific condition.
    """)
    
    # SQL Query
    sql_command = """
    CREATE TABLE employees (
        emp_id INT PRIMARY KEY,
        name VARCHAR(50),
        department VARCHAR(50),
        salary DECIMAL(10, 2) CHECK (salary > 30000)
    );
    """
    st.code(sql_command, language="sql")
    
    st.markdown("### Add New Employee with Salary Check")
    new_emp_id = st.number_input("Employee ID:", min_value=1, step=1, key="check_emp_id")
    new_name = st.text_input("Name:", key="check_name")
    new_department = st.text_input("Department:", key="check_department")
    new_salary = st.number_input("Salary (Must be > 30000):", min_value=1, step=1, key="check_salary")
    
    if st.button("Add Row", key="check_key"):
        if new_salary <= 30000:
            st.error(f"❌ Salary '{new_salary}' does not meet the CHECK constraint (salary > 30000).")
        else:
            new_row = pd.DataFrame({
                'emp_id': [new_emp_id],
                'name': [new_name],
                'department': [new_department],
                'salary': [new_salary]
            })
            employees = pd.concat([employees, new_row], ignore_index=True)
            st.success("✅ Row added successfully! CHECK constraint maintained.")
        st.dataframe(employees)

# NOT NULL
with tabs[4]:
    st.header("🚫 NOT NULL Constraint")
    st.markdown("""
    The `NOT NULL` constraint ensures that a column cannot have a `NULL` value.
    """)
    
    # SQL Query
    sql_command = """
    CREATE TABLE employees (
        emp_id INT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        department VARCHAR(50),
        salary DECIMAL(10, 2)
    );
    """
    st.code(sql_command, language="sql")
    
    st.markdown("### Add New Employee with Name Not Null")
    new_emp_id = st.number_input("Employee ID:", min_value=1, step=1, key="notnull_emp_id")
    new_name = st.text_input("Name (Cannot be NULL):", key="notnull_name")
    new_department = st.text_input("Department:", key="notnull_department")
    new_salary = st.number_input("Salary:", min_value=1, step=1, key="notnull_salary")
    
    if st.button("Add Row", key="notnull_key"):
        if new_name.strip() == "":
            st.error("❌ Name cannot be NULL or empty. NOT NULL constraint violated.")
        else:
            new_row = pd.DataFrame({
                'emp_id': [new_emp_id],
                'name': [new_name],
                'department': [new_department],
                'salary': [new_salary]
            })
            employees = pd.concat([employees, new_row], ignore_index=True)
            st.success("✅ Row added successfully! NOT NULL constraint maintained.")
        st.dataframe(employees)

# DEFAULT
with tabs[5]:
    st.header("📥 DEFAULT Constraint")
    st.markdown("""
    The `DEFAULT` constraint assigns a default value to a column when no value is provided.
    """)
    
    # SQL Query
    sql_command = """
    CREATE TABLE employees (
        emp_id INT PRIMARY KEY,
        name VARCHAR(50),
        department VARCHAR(50),
        salary DECIMAL(10, 2) DEFAULT 40000
    );
    """
    st.code(sql_command, language="sql")
    
    st.markdown("### Add New Employee with Default Salary")
    new_emp_id = st.number_input("Employee ID:", min_value=1, step=1, key="default_emp_id")
    new_name = st.text_input("Name:", key="default_name")
    new_department = st.text_input("Department:", key="default_department")
    new_salary = st.number_input("Salary (Leave blank for default):", min_value=0, step=1, key="default_salary", value=0)
    
    if st.button("Add Row", key="default_key"):
        salary_to_insert = new_salary if new_salary != 0 else 40000
        new_row = pd.DataFrame({
            'emp_id': [new_emp_id],
            'name': [new_name],
            'department': [new_department],
            'salary': [salary_to_insert]
        })
        employees = pd.concat([employees, new_row], ignore_index=True)
        st.success("✅ Row added successfully! DEFAULT constraint applied where necessary.")
        st.dataframe(employees)

# Footer Quiz Section
st.markdown("---")
st.header("🎯 Test Your Knowledge!")

quiz_question = st.multiselect(
    "Which constraint cannot have a NULL value?",
    ["PRIMARY KEY", "NOT NULL", "UNIQUE", "DEFAULT"],
    key="constraints_quiz"
)

if st.button("Submit Answer", key="constraints_quiz_submit"):
    correct_answers = {"PRIMARY KEY", "NOT NULL"}  # Set of correct answers
    selected_answers = set(quiz_question)  # Convert user selection to a set
    
    if selected_answers == correct_answers:
        st.success("Correct! 🎉 Both PRIMARY KEY and NOT NULL cannot have NULL values.")
    else:
        missing_answers = correct_answers
        extra_answers = selected_answers - correct_answers

        feedback = "Oops! You got it wrong:\n"
        if missing_answers:
            feedback += f"- Correct answer(s): {', '.join(missing_answers)}\n"
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