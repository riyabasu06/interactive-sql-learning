import streamlit as st
import pandas as pd

# Title and Introduction
st.title("🔄 Stored Procedures and Functions")
st.markdown("""
Welcome to the interactive SQL tutorial on **Stored Procedures and Functions**! 🚀

Stored procedures and functions allow you to encapsulate SQL logic for reuse, making your database queries more efficient and organized.

---

### What We'll Cover:
1. Creating Stored Procedures
2. Creating Functions
3. Parameters in Stored Procedures and Functions
4. Handling Errors in Stored Procedures
5. The CALL Statement
6. Differences Between Procedures and Functions

---

Here's a sample table to help us understand the concepts:
""")

# Sample Data
employees = pd.DataFrame({
    'emp_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'department': ['HR', 'Engineering', 'Marketing', 'Engineering'],
    'salary': [50000, 60000, 55000, 70000]
})

st.subheader("Employee Table")
st.dataframe(employees)

# Tabs for Subtopics
tabs = st.tabs([
    "Creating Stored Procedures", "Creating Functions", "Parameters", 
    "Error Handling", "CALL Statement", "Differences"
])

# Creating Stored Procedures
with tabs[0]:
    st.header("🔧 Creating Stored Procedures")
    st.markdown("""
    **Definition**: A stored procedure is a precompiled SQL code that can be executed repeatedly.

    **SQL Syntax**:
    ```sql
    CREATE PROCEDURE procedure_name (parameters)
    BEGIN
        SQL statements;
    END;
    ```

    **Example**: Create a procedure to retrieve employees by department.
    """)

    sql_command = """
    CREATE PROCEDURE GetEmployeesByDepartment(IN dept_name VARCHAR(50))
    BEGIN
        SELECT emp_id, name, salary
        FROM employees
        WHERE department = dept_name;
    END;
    """
    st.code(sql_command, language="sql")

    st.markdown("### Interactive Example")
    selected_department = st.selectbox("Select a Department to Call the Procedure:", employees['department'].unique())
    result = employees[employees['department'] == selected_department]
    st.markdown(f"**Results for `{selected_department}` Department:**")
    st.dataframe(result)

# Creating Functions
with tabs[1]:
    st.header("🔧 Creating Functions")
    st.markdown("""
    **Definition**: A function is a reusable SQL object that returns a single value.

    **SQL Syntax**:
    ```sql
    CREATE FUNCTION function_name (parameters)
    RETURNS datatype
    BEGIN
        SQL statements;
        RETURN value;
    END;
    ```

    **Example**: Create a function to calculate an annual salary.
    """)

    sql_command = """
    CREATE FUNCTION GetAnnualSalary(emp_salary DECIMAL(10, 2))
    RETURNS DECIMAL(10, 2)
    BEGIN
        RETURN emp_salary * 12;
    END;
    """
    st.code(sql_command, language="sql")

    st.markdown("### Interactive Example")
    emp_salary = st.number_input("Enter Monthly Salary:", min_value=0, step=1000, value=50000)
    annual_salary = emp_salary * 12
    st.markdown(f"**Annual Salary for Monthly Salary `{emp_salary}` is `{annual_salary}`.**")

# Parameters in Procedures and Functions
with tabs[2]:
    st.header("⚙️ Parameters in Procedures and Functions")
    st.markdown("""
    Parameters allow data to be passed into and out of stored procedures and functions.

    **Types of Parameters**:
    - `IN`: Passes input values to the procedure.
    - `OUT`: Returns output values from the procedure.
    - `INOUT`: Acts as both input and output.

    **Example**: Procedure to calculate bonus based on a percentage.
    """)

    sql_command = """
    CREATE PROCEDURE CalculateBonus(IN emp_salary DECIMAL(10, 2), IN bonus_percent DECIMAL(5, 2), OUT bonus_amount DECIMAL(10, 2))
    BEGIN
        SET bonus_amount = emp_salary * (bonus_percent / 100);
    END;
    """
    st.code(sql_command, language="sql")

    st.markdown("### Interactive Example")
    emp_salary = st.number_input("Enter Employee Salary:", min_value=0, step=1000, value=50000, key="bonus_salary")
    bonus_percent = st.number_input("Enter Bonus Percentage:", min_value=0.0, step=1.0, value=10.0)
    bonus_amount = emp_salary * (bonus_percent / 100)
    st.markdown(f"**Bonus Amount for `{bonus_percent}%` Bonus: `{bonus_amount}`**")

# Error Handling
with tabs[3]:
    st.header("⚠️ Handling Errors in Stored Procedures")
    st.markdown("""
    Error handling allows you to catch and handle errors during procedure execution.

    **SQL Syntax**:
    ```sql
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Error handling code
    END;
    ```

    **Example**: Handle division by zero in a procedure.
    """)

    sql_command = """
    CREATE PROCEDURE SafeDivision(IN numerator DECIMAL(10, 2), IN denominator DECIMAL(10, 2), OUT result DECIMAL(10, 2))
    BEGIN
        DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
        SET result = NULL;
        IF denominator = 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Division by zero is not allowed';
        ELSE
            SET result = numerator / denominator;
        END IF;
    END;
    """
    st.code(sql_command, language="sql")

    st.markdown("### Interactive Example")
    numerator = st.number_input("Enter Numerator:", min_value=0, step=1, value=10, key="numerator")
    denominator = st.number_input("Enter Denominator:", min_value=0, step=1, value=2, key="denominator")
    if denominator == 0:
        st.error("❌ Division by zero is not allowed!")
    else:
        division_result = numerator / denominator
        st.markdown(f"**Result: `{division_result}`**")

# CALL Statement
with tabs[4]:
    st.header("📞 CALL Statement")
    st.markdown("""
    The `CALL` statement is used to execute a stored procedure.

    **SQL Syntax**:
    ```sql
    CALL procedure_name(parameters);
    ```

    **Example**: Call the `GetEmployeesByDepartment` procedure.
    """)

    sql_command = """
    CALL GetEmployeesByDepartment('Engineering');
    """
    st.code(sql_command, language="sql")

# Differences Between Procedures and Functions
with tabs[5]:
    st.header("⚖️ Differences Between Procedures and Functions")
    st.markdown("""
    | Aspect                  | Procedures                           | Functions                          |
    |-------------------------|---------------------------------------|------------------------------------|
    | **Purpose**             | Perform actions                     | Return a single value             |
    | **Invocation**          | `CALL procedure_name`                | Part of an SQL query              |
    | **Output**              | Can return multiple values           | Returns one value                 |
    | **Usage in Queries**    | Cannot be used in queries directly   | Can be used in SELECT statements  |
    | **Error Handling**      | Explicit error handling              | Implicit error handling           |

    ### Summary:
    - Use **procedures** for complex operations.
    - Use **functions** for reusable calculations.
    """)

# Footer Quiz Section
st.markdown("---")
st.header("🎯 Test Your Knowledge!")
quiz_question = st.multiselect(
    "Which statements about procedures and functions are true? (Select all that apply)",
    [
        "A procedure can return multiple values.",
        "A function can return multiple values.",
        "Functions can be used in SELECT statements.",
        "Procedures can handle complex operations."
    ],
    key="quiz_procedures"
)

if st.button("Submit Answer", key="quiz_submit"):
    correct_answers = {
        "A procedure can return multiple values.",
        "Functions can be used in SELECT statements.",
        "Procedures can handle complex operations."
    }
    selected_answers = set(quiz_question)

    if selected_answers == correct_answers:
        st.success("Correct! 🎉 Functions and procedures have distinct use cases.")
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