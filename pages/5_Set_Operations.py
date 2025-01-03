import streamlit as st
import pandas as pd

# Sample Data for Demonstration
employees_a = pd.DataFrame({
    'emp_id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie'],
    'department': ['HR', 'Engineering', 'Marketing'],
    'salary': [50000, 60000, 55000]
})

employees_b = pd.DataFrame({
    'emp_id': [3, 4, 5],
    'name': ['Charlie', 'David', 'Eva'],
    'department': ['Marketing', 'Engineering', 'HR'],
    'salary': [55000, 70000, 48000]
})

# Title and Introduction
st.title("🔗 SQL Set Operations")
st.markdown("""
Welcome to the interactive SQL Set Operations tutorial! 🚀

Set operations allow you to combine the results of two or more queries into a single result. The four key operations are:
- `UNION`
- `UNION ALL`
- `INTERSECT`
- `EXCEPT` (or `MINUS` in some databases)

---

Here are the sample tables we will work with:
""")

# Display Sample Tables
st.subheader("Employees Table A")
st.dataframe(employees_a)

st.subheader("Employees Table B")
st.dataframe(employees_b)

# Tabs for Subtopics
tabs = st.tabs(["UNION", "UNION ALL", "INTERSECT", "EXCEPT (MINUS)"])

# UNION
with tabs[0]:
    st.header("🔗 UNION Operation")
    st.markdown("""
    The `UNION` operator combines the results of two queries and removes duplicate rows. 
    Both queries must return the same number of columns, with matching data types.
    """)
    selected_columns = st.multiselect(
        "Choose columns to include in the UNION:",
        employees_a.columns,
        default=employees_a.columns
    )
    if selected_columns:
        union_result = pd.concat([employees_a[selected_columns], employees_b[selected_columns]]).drop_duplicates().reset_index(drop=True)
        sql_command = f"""
        SELECT {', '.join(selected_columns)}
        FROM employees_a
        UNION
        SELECT {', '.join(selected_columns)}
        FROM employees_b;
        """
        
        st.code(sql_command, language="sql")
        st.markdown("**Result:**")
        st.dataframe(union_result)

# UNION ALL
with tabs[1]:
    st.header("🔗 UNION ALL Operation")
    st.markdown("""
    The `UNION ALL` operator combines the results of two queries, including all duplicate rows.
    """)
    selected_columns = st.multiselect(
        "Choose columns to include in the UNION ALL:",
        employees_a.columns,
        default=employees_a.columns,
        key="union_all_columns"
    )
    if selected_columns:
        union_all_result = pd.concat([employees_a[selected_columns], employees_b[selected_columns]]).reset_index(drop=True)
        sql_command = f"""
        SELECT {', '.join(selected_columns)}
        FROM employees_a
        UNION ALL
        SELECT {', '.join(selected_columns)}
        FROM employees_b;
        """
        
        st.code(sql_command, language="sql")
        st.markdown("**Result:**")
        st.dataframe(union_all_result)

# INTERSECT
with tabs[2]:
    st.header("🔗 INTERSECT Operation")
    st.markdown("""
    The `INTERSECT` operator returns rows that are present in both queries.
    """)
    selected_columns = st.multiselect(
        "Choose columns to include in the INTERSECT:",
        employees_a.columns,
        default=employees_a.columns,
        key="intersect_columns"
    )
    if selected_columns:
        intersect_result = pd.merge(
            employees_a[selected_columns], employees_b[selected_columns], how="inner"
        )
        sql_command = f"""
        SELECT {', '.join(selected_columns)}
        FROM employees_a
        INTERSECT
        SELECT {', '.join(selected_columns)}
        FROM employees_b;
        """
        
        st.code(sql_command, language="sql")
        st.markdown("**Result:**")
        st.dataframe(intersect_result)

# EXCEPT (MINUS)
with tabs[3]:
    st.header("🔗 EXCEPT (MINUS) Operation")
    st.markdown("""
    The `EXCEPT` operator (or `MINUS` in some databases) returns rows from the first query that are not present in the second query.
    """)
    selected_columns = st.multiselect(
        "Choose columns to include in the EXCEPT:",
        employees_a.columns,
        default=employees_a.columns,
        key="except_columns"
    )
    if selected_columns:
        except_result = employees_a[selected_columns].merge(
            employees_b[selected_columns], how="outer", indicator=True
        )
        except_result = except_result[except_result['_merge'] == 'left_only'].drop('_merge', axis=1)
        sql_command = f"""
        SELECT {', '.join(selected_columns)}
        FROM employees_a
        EXCEPT
        SELECT {', '.join(selected_columns)}
        FROM employees_b;
        """
        
        st.code(sql_command, language="sql")
        st.markdown("**Result:**")
        st.dataframe(except_result)

# Footer Quiz Section
st.markdown("---")
st.header("🎯 Test Your Knowledge!")
quiz_question = st.radio(
    "Which SQL operation includes all rows from both queries, even duplicates?",
    ["UNION", "UNION ALL", "INTERSECT", "EXCEPT"],
    key="set_operations_quiz"
)
if st.button("Submit Answer", key="set_operations_quiz_submit"):
    if quiz_question == "UNION ALL":
        st.success("Correct! 🎉 The UNION ALL operation includes all rows, even duplicates.")
    else:
        st.error("Oops! Try again. Hint: Think about which operation retains duplicates.")

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
