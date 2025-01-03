import streamlit as st
import pandas as pd

# Sample Data for Demonstration
data = pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 6],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank'],
    'age': [25, 35, 30, 40, 29, 35],
    'department': ['HR', 'Engineering', 'Marketing', 'Engineering', 'HR', 'Marketing'],
    'salary': [50000, 60000, 55000, 70000, 48000, 62000]
})

# Title and Introduction
st.title("📊 Aggregating Data")
st.markdown("""
Welcome to the interactive tutorial on **Aggregating Data in SQL**! 🚀 

Aggregation functions in SQL allow you to perform calculations on a set of values and return a single value. 
These are particularly useful in summarizing data, analyzing trends, and generating reports.

""")

# Tabs for Subtopics
tabs = st.tabs(["COUNT()", "SUM()", "AVG()", "MIN()", "MAX()", "GROUP BY", "HAVING Clause"])

# COUNT()
with tabs[0]:
    st.header("🔢 COUNT() Function")
    st.markdown("""
    The `COUNT()` function returns the number of rows that match a specified condition.
    
    **SQL Syntax:**
    ```sql
    SELECT COUNT(column_name) FROM table_name WHERE condition;
    ```
    """)
    st.subheader("Sample Table")
    st.dataframe(data)
    st.subheader("Example")
    
    # User selects a column to count
    selected_column = st.selectbox("Choose a column to count:", data.columns)
    
    # Generate SQL query based on selection
    sql_command = f"SELECT COUNT({selected_column}) FROM table_name;"
    
    # Display the count and the SQL command
    st.write(f"**Result:** Number of non-null values in `{selected_column}`: **{data[selected_column].count()}**")
    st.code(sql_command, language="sql")


# SUM()
with tabs[1]:
    st.header("➕ SUM() Function")
    st.markdown("""
    The `SUM()` function returns the total sum of a numeric column.
    
    **SQL Syntax:**
    ```sql
    SELECT SUM(column_name) FROM table_name;
    ```
    """)
    st.subheader("Sample Table")
    st.dataframe(data)
    
    st.subheader("Example")
    
    # User selects a numeric column
    sum_column = st.selectbox("Choose a column to sum:", data.select_dtypes(include='number').columns)
    
    # Compute the total sum
    total_sum = data[sum_column].sum()
    st.write(f"**Total sum of `{sum_column}`: {total_sum}**")
    
    # Generate dynamic SQL query
    sql_command = f"SELECT SUM({sum_column}) FROM table_name;"
    st.code(sql_command, language="sql")

# AVG()
with tabs[2]:
    st.header("🔢 AVG() Function")
    st.markdown("""
    The `AVG()` function calculates the average value of a numeric column.
    
    **SQL Syntax:**
    ```sql
    SELECT AVG(column_name) FROM table_name WHERE condition;
    ```
    """)
    st.subheader("Sample Table")
    st.dataframe(data)
    st.subheader("Example")
    avg_column = st.selectbox("Choose a column to calculate the average:", data.select_dtypes(include='number').columns)
    st.write(f"Average of `{avg_column}`: **{data[avg_column].mean()}**")

    # Generate dynamic SQL query
    sql_command = f"SELECT AVG({avg_column}) FROM table_name;"
    st.code(sql_command, language="sql")

# MIN()
with tabs[3]:
    st.header("🔽 MIN() Function")
    st.markdown("""
    The `MIN()` function returns the smallest value in a column.
    
    **SQL Syntax:**
    ```sql
    SELECT MIN(column_name) FROM table_name WHERE condition;
    ```
    """)
    st.subheader("Sample Table")
    st.dataframe(data)
    st.subheader("Example")
    min_column = st.selectbox("Choose a column to find the minimum:", data.select_dtypes(include='number').columns)
    st.write(f"Minimum value in `{min_column}`: **{data[min_column].min()}**")

    # Generate dynamic SQL query
    sql_command = f"SELECT MIN({min_column}) FROM table_name;"
    st.code(sql_command, language="sql")

# MAX()
with tabs[4]:
    st.header("🔼 MAX() Function")
    st.markdown("""
    The `MAX()` function returns the largest value in a column.
    
    **SQL Syntax:**
    ```sql
    SELECT MAX(column_name) FROM table_name WHERE condition;
    ```
    """)
    st.subheader("Sample Table")
    st.dataframe(data)
    st.subheader("Example")
    max_column = st.selectbox("Choose a column to find the maximum:", data.select_dtypes(include='number').columns)
    st.write(f"Maximum value in `{max_column}`: **{data[max_column].max()}**")

    # Generate dynamic SQL query
    sql_command = f"SELECT MAX({max_column}) FROM table_name;"
    st.code(sql_command, language="sql")

with tabs[5]:
    st.header("🧮 GROUP BY Clause")
    st.markdown("""
    The `GROUP BY` clause groups rows that have the same values in specified columns into summary rows, such as "total salary by department".
    
    **SQL Syntax:**
    ```sql
    SELECT column_name, aggregation_function(column_name)
    FROM table_name
    GROUP BY column_name;
    ```
    """)
    st.subheader("Sample Table")
    st.dataframe(data)
    
    st.subheader("Example")
    
    # User selects a column to group by
    group_by_column = st.selectbox("Choose a column to group by:", data.columns)
    
    # User selects an aggregation function
    aggregation_function = st.radio("Choose an aggregation function:", ["SUM", "AVG", "COUNT", "MAX", "MIN"])
    
    # Perform the aggregation and group by operation
    if aggregation_function == "SUM":
        grouped_result = data.groupby(group_by_column)['salary'].sum().reset_index(name='Total Salary')
        sql_command = f"SELECT {group_by_column}, SUM(salary) AS Total_Salary FROM table_name GROUP BY {group_by_column};"
    elif aggregation_function == "AVG":
        grouped_result = data.groupby(group_by_column)['salary'].mean().reset_index(name='Average Salary')
        sql_command = f"SELECT {group_by_column}, AVG(salary) AS Average_Salary FROM table_name GROUP BY {group_by_column};"
    elif aggregation_function == "COUNT":
        grouped_result = data.groupby(group_by_column)['salary'].count().reset_index(name='Count')
        sql_command = f"SELECT {group_by_column}, COUNT(salary) AS Count FROM table_name GROUP BY {group_by_column};"
    elif aggregation_function == "MAX":
        grouped_result = data.groupby(group_by_column)['salary'].max().reset_index(name='Max Salary')
        sql_command = f"SELECT {group_by_column}, MAX(salary) AS Max_Salary FROM table_name GROUP BY {group_by_column};"
    elif aggregation_function == "MIN":
        grouped_result = data.groupby(group_by_column)['salary'].min().reset_index(name='Min Salary')
        sql_command = f"SELECT {group_by_column}, MIN(salary) AS Min_Salary FROM table_name GROUP BY {group_by_column};"
    
    # Display the grouped result and the SQL query
    st.dataframe(grouped_result)
    st.code(sql_command, language="sql")


with tabs[6]:
    st.header("🛑 HAVING Clause")
    st.markdown("""
    The `HAVING` clause is used to filter groups of rows based on aggregate functions, unlike the `WHERE` clause which filters individual rows.
    
    **SQL Syntax:**
    ```sql
    SELECT column_name, aggregation_function(column_name)
    FROM table_name
    GROUP BY column_name
    HAVING aggregation_function(column_name) condition;
    ```
    """)
    st.subheader("Sample Table")
    st.dataframe(data)

    st.subheader("Example")

    # User selects a column to group by
    group_by_column = st.selectbox("Choose a column to group by:", data.columns, key="having_group_by_column")

    # User selects an aggregation function
    aggregation_function = st.radio("Choose an aggregation function:", ["SUM", "AVG", "MAX", "MIN"], key="having_aggregation_function")

    # User sets a condition for the HAVING clause
    condition_value = st.number_input("Enter the condition value (e.g., 100000):", value=100000, step=1000, key="having_condition_value")

    # Perform the aggregation and filter using HAVING condition
    if aggregation_function == "SUM":
        grouped_result = data.groupby(group_by_column)['salary'].sum().reset_index(name='Total Salary')
        filtered_result = grouped_result[grouped_result['Total Salary'] > condition_value]
        sql_command = f"SELECT {group_by_column}, SUM(salary) AS Total_Salary FROM table_name GROUP BY {group_by_column} HAVING SUM(salary) > {condition_value};"
    elif aggregation_function == "AVG":
        grouped_result = data.groupby(group_by_column)['salary'].mean().reset_index(name='Average Salary')
        filtered_result = grouped_result[grouped_result['Average Salary'] > condition_value]
        sql_command = f"SELECT {group_by_column}, AVG(salary) AS Average_Salary FROM table_name GROUP BY {group_by_column} HAVING AVG(salary) > {condition_value};"
    elif aggregation_function == "MAX":
        grouped_result = data.groupby(group_by_column)['salary'].max().reset_index(name='Max Salary')
        filtered_result = grouped_result[grouped_result['Max Salary'] > condition_value]
        sql_command = f"SELECT {group_by_column}, MAX(salary) AS Max_Salary FROM table_name GROUP BY {group_by_column} HAVING MAX(salary) > {condition_value};"
    elif aggregation_function == "MIN":
        grouped_result = data.groupby(group_by_column)['salary'].min().reset_index(name='Min Salary')
        filtered_result = grouped_result[grouped_result['Min Salary'] > condition_value]
        sql_command = f"SELECT {group_by_column}, MIN(salary) AS Min_Salary FROM table_name GROUP BY {group_by_column} HAVING MIN(salary) > {condition_value};"

    # Display the grouped result and the SQL query
    st.dataframe(filtered_result)
    st.code(sql_command, language="sql")


# Footer Quiz Section
st.markdown("---")
st.header("🎯 Test Your Knowledge!")
quiz_question = st.radio(
    "Which clause is used to filter groups of rows based on aggregate functions?",
    ["GROUP BY", "WHERE", "HAVING"]
)
if st.button("Submit Answer"):
    if quiz_question == "HAVING":
        st.success("Correct! 🎉 The HAVING clause filters groups based on aggregate functions.")
    else:
        st.error("Oops! Try again. Hint: It's used after GROUP BY. 😉")

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
