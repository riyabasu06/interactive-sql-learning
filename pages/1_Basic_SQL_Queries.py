import streamlit as st
import pandas as pd

# Sample data for demonstrations
data = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'age': [25, 35, 30, 40, 29],
    'department': ['HR', 'Engineering', 'Marketing', 'Engineering', 'HR'],
    'city': ['New York', 'Los Angeles', 'Chicago', 'San Francisco', 'New York']
})

# Title and Introduction
st.title("🎓 Basic SQL Queries")
st.markdown("""
Welcome to this interactive SQL tutorial! 🚀 Here, you'll learn SQL basics, one concept at a time, 
and see their practical application through hands-on examples. 

Let's begin! 🐱‍💻
---
""")

# SQL Subtopics as Tabs
tabs = st.tabs(["SELECT", "WHERE", "ORDER BY", "DISTINCT", "LIMIT", "LIKE", "IN", "BETWEEN"])

# SELECT Statement
with tabs[0]:
    st.header("🔍 SELECT Statement")
    st.markdown("""
    The `SELECT` statement retrieves data from a database table. 
    Example:
    ```sql
    SELECT column1, column2 FROM table_name;
    ```
    """)
    columns = st.multiselect("Select columns to display:", data.columns, default=data.columns)
    st.dataframe(data[columns])


# WHERE Clause
with tabs[1]:
    st.header("🔍 WHERE Clause")
    st.markdown("""
    Use the `WHERE` clause to filter rows based on conditions.
    Example:
    ```sql
    SELECT * FROM table_name WHERE condition;
    ```
    """)
    column_filter = st.selectbox("Choose a column to filter:", data.columns)
    value_filter = st.text_input("Enter a value to filter by (e.g., Engineering or 30):")
    
    if value_filter:  # Proceed only if a filter value is provided
        # Check the data type of the selected column
        if pd.api.types.is_numeric_dtype(data[column_filter]):
            # Convert input value to numeric
            try:
                value_filter = float(value_filter)  # Convert to float to handle integers and decimals
                filtered_data = data[data[column_filter] == value_filter]

                sql_command = f"SELECT * FROM table_name WHERE {column_filter} = {value_filter};"
            except ValueError:
                st.error("Invalid input for a numeric column. Please enter a number.")
                filtered_data = data
                sql_command = f"-- Invalid input. Could not generate SQL command."
        else:
            # For non-numeric columns, use string comparison
            filtered_data = data[data[column_filter] == value_filter]
            sql_command = f"SELECT * FROM table_name WHERE {column_filter} = '{value_filter}';"
    else:
        filtered_data = data  # Show all data if no filter is applied
        sql_command = "SELECT * FROM table_name; -- No filter applied"
    # Generate SQL query based on selection
    st.code(sql_command, language="sql")
    st.dataframe(filtered_data)

# ORDER BY Clause
with tabs[2]:
    st.header("🔍 ORDER BY Clause")
    st.markdown("""
    Use `ORDER BY` to sort query results.
    Example:
    ```sql
    SELECT * FROM table_name ORDER BY column_name ASC/DESC;
    ```
    """)
    sort_column = st.selectbox("Choose a column to sort by:", data.columns)
    sort_order = st.radio("Sort order:", ['Ascending', 'Descending'])
    sorted_data = data.sort_values(by=sort_column, ascending=(sort_order == 'Ascending'))
    st.dataframe(sorted_data)

# DISTINCT Keyword
with tabs[3]:
    st.header("🔍 DISTINCT Keyword")
    st.markdown("""
    The `DISTINCT` keyword returns unique values from a column.
    Example:
    ```sql
    SELECT DISTINCT column_name FROM table_name;
    ```
    """)
    distinct_column = st.selectbox("Choose a column to find unique values:", data.columns)
    distinct_values = data[distinct_column].drop_duplicates()
    st.dataframe(distinct_values)

# LIMIT Clause
with tabs[4]:
    st.header("🔍 LIMIT Clause")
    st.markdown("""
    Use the `LIMIT` clause to restrict the number of rows returned.
    Example:
    ```sql
    SELECT * FROM table_name LIMIT number;
    ```
    """)
    limit_rows = st.slider("Number of rows to display:", min_value=1, max_value=len(data), value=5)
    st.dataframe(data.head(limit_rows))

# LIKE Operator
with tabs[5]:
    st.header("🔍 LIKE Operator")
    st.markdown("""
    The `LIKE` operator filters rows based on patterns in text data. It allows for flexible matching, such as finding 
    rows where a value begins with, ends with, or contains a specific substring.

    Example:
    ```sql
    SELECT * FROM table_name WHERE column_name LIKE 'pattern';
    ```
    """)
    
    # Select column for LIKE operation
    like_column = st.selectbox("Choose a column to apply pattern matching:", data.select_dtypes(include='object').columns)
    
    # Choose pattern type
    pattern_type = st.radio("Choose a pattern type:", ["Contains", "Begins with", "Ends with", "Exact Match"])
    
    # Enter pattern input
    user_input = st.text_input("Enter the pattern to match:")
    
    # Determine SQL pattern and regex based on selection
    sql_syntax = ""
    if pattern_type == "Contains":
        pattern = f".*{user_input}.*"  # Regex for contains
        sql_syntax = f"SELECT * FROM table_name WHERE {like_column} LIKE '%{user_input}%';"
    elif pattern_type == "Begins with":
        pattern = f"^{user_input}.*"  # Regex for begins with
        sql_syntax = f"SELECT * FROM table_name WHERE {like_column} LIKE '{user_input}%';"
    elif pattern_type == "Ends with":
        pattern = f".*{user_input}$"  # Regex for ends with
        sql_syntax = f"SELECT * FROM table_name WHERE {like_column} LIKE '%{user_input}';"
    elif pattern_type == "Exact Match":
        pattern = f"^{user_input}$"  # Regex for exact match
        sql_syntax = f"SELECT * FROM table_name WHERE {like_column} = '{user_input}';"
    
    # Display SQL syntax for the selected pattern
    st.markdown(f"**SQL Syntax:**")
    st.code(sql_syntax, language="sql")
    
    # Filter data using regex
    if user_input:
        like_filtered_data = data[data[like_column].str.contains(pattern, na=False, regex=True)]
    else:
        like_filtered_data = data  # Show all data if no input
    
    # Display filtered data
    st.dataframe(like_filtered_data)

# IN Operator
with tabs[6]:
    st.header("🔍 IN Operator")
    st.markdown("""
    Use the `IN` operator to filter rows where a column matches any value in a list.
    Example:
    ```sql
    SELECT * FROM table_name WHERE column_name IN ('value1', 'value2');
    ```
    """)
    in_column = st.selectbox("Choose a column for filtering:", data.columns)
    in_values = st.text_input("Enter values to match (comma-separated):", "Engineering, HR")
    values_list = [v.strip() for v in in_values.split(',')]
    in_filtered_data = data[data[in_column].isin(values_list)] if in_values else data
    st.dataframe(in_filtered_data)

# BETWEEN Operator
with tabs[7]:
    st.header("🔍 BETWEEN Operator")
    st.markdown("""
    The `BETWEEN` operator filters rows within a range of values.
    Example:
    ```sql
    SELECT * FROM table_name WHERE column_name BETWEEN value1 AND value2;
    ```
    """)
    between_column = st.selectbox("Choose a column for range filtering:", data.select_dtypes(include='number').columns)
    min_value, max_value = st.slider("Select range:", min_value=int(data[between_column].min()), 
                                     max_value=int(data[between_column].max()), 
                                     value=(int(data[between_column].min()), int(data[between_column].max())))
    between_filtered_data = data[(data[between_column] >= min_value) & (data[between_column] <= max_value)]
    st.dataframe(between_filtered_data)

# Footer Quiz Section
st.markdown("---")
st.header("🎯 Test Your Knowledge!")
quiz_question = st.radio(
    "Which SQL clause is used to filter rows based on conditions?",
    ["SELECT", "WHERE", "DISTINCT", "LIMIT"]
)
if st.button("Submit Answer"):
    if quiz_question == "WHERE":
        st.success("Correct! 🎉 The WHERE clause filters rows based on conditions.")
    else:
        st.error("Try again! Hint: It starts with 'W'. 😉")

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
