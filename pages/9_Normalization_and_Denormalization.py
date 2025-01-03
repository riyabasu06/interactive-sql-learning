import streamlit as st
import pandas as pd

# Title and Introduction
st.title("📚 Normalization and Denormalization ")
st.markdown("""
Welcome to the interactive SQL Normalization and Denormalization tutorial! 🚀

- **Normalization**: The process of organizing data to minimize redundancy.
- **Denormalization**: The process of combining tables to improve query performance.

---

### What We'll Cover:
1. First Normal Form (1NF)
2. Second Normal Form (2NF)
3. Third Normal Form (3NF)
4. Boyce-Codd Normal Form (BCNF)
5. Denormalization Techniques
6. Benefits and Trade-offs of Normalization vs. Denormalization

---

Here’s the unnormalized sample data we'll work with:
""")

# Unnormalized Data
unnormalized_data = pd.DataFrame({
    'emp_id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'department': ['HR', 'Engineering', 'Engineering', 'Marketing'],
    'project': ['Recruitment', 'Project A, Project B', 'Project B', 'Ad Campaign'],
    'salary': [50000, 60000, 55000, 70000],
    'manager': ['Eve', 'Tom', 'Tom', 'Susan']
})
st.subheader("Unnormalized Data")
st.dataframe(unnormalized_data)

# Tabs for Subtopics
tabs = st.tabs([
    "First Normal Form (1NF)", "Second Normal Form (2NF)", "Third Normal Form (3NF)",
    "Boyce-Codd Normal Form (BCNF)", "Denormalization Techniques", "Benefits & Trade-offs"
])

# First Normal Form (1NF)
with tabs[0]:
    st.header("🔹 First Normal Form (1NF)")
    st.markdown("""
    **Definition**: A table is in the First Normal Form if:
    - Each column contains atomic (indivisible) values.
    - Each row is unique.

    **Unnormalized Problem**: Multiple projects assigned to a single employee are stored in one row, violating atomicity.
    
    **Solution**: Split multiple values into separate rows.
    """)
    # Normalize to 1NF
    data_1nf = pd.DataFrame({
        'emp_id': [1, 2, 2, 3, 4],
        'name': ['Alice', 'Bob', 'Bob', 'Charlie', 'David'],
        'department': ['HR', 'Engineering', 'Engineering', 'Engineering', 'Marketing'],
        'project': ['Recruitment', 'Project A', 'Project B', 'Project B', 'Ad Campaign'],
        'salary': [50000, 60000, 60000, 55000, 70000],
        'manager': ['Eve', 'Tom', 'Tom', 'Tom', 'Susan']
    })
    st.subheader("Normalized to 1NF")
    st.dataframe(data_1nf)

    sql_command = """
    SELECT emp_id, name, department, project, salary, manager
    FROM unnormalized_table
    WHERE project IS NOT NULL;
    """
    st.markdown("**SQL Query to Normalize to 1NF:**")
    st.code(sql_command, language="sql")

# Second Normal Form (2NF)
with tabs[1]:
    st.header("🔹 Second Normal Form (2NF)")
    st.markdown("""
    **Definition**: A table is in the Second Normal Form if:
    - It is in 1NF.
    - All non-key columns are fully functionally dependent on the primary key.

    **Problem**: The `department` and `manager` columns depend only on `department` and not the full composite key (`emp_id`, `project`).
    
    **Solution**: Decompose the table into two tables:
    - One for employee-project details.
    - Another for department-manager relationships.
    """)

    project_table = pd.DataFrame({
        'emp_id': [1, 2, 2, 3, 4],
        'project': ['Recruitment', 'Project A', 'Project B', 'Project B', 'Ad Campaign'],
        'salary': [50000, 60000, 60000, 70000, 48000]
    })

    department_table = pd.DataFrame({
        'department': ['HR', 'Engineering', 'Marketing'],
        'manager': ['Eve', 'Tom', 'Susan']
    })

    st.subheader("Employee-Project Table")
    st.dataframe(project_table)

    st.subheader("Department-Manager Table")
    st.dataframe(department_table)

    sql_command = """
    CREATE TABLE project_details (
        emp_id INT,
        project VARCHAR(50),
        salary DECIMAL(10, 2)
    );

    CREATE TABLE department_manager (
        department VARCHAR(50),
        manager VARCHAR(50)
    );
    """
    st.markdown("**SQL Queries to Normalize to 2NF:**")
    st.code(sql_command, language="sql")

# Third Normal Form (3NF)
with tabs[2]:
    st.header("🔹 Third Normal Form (3NF)")
    st.markdown("""
    **Definition**: A table is in the Third Normal Form if:
    - It is in 2NF.
    - No transitive dependencies exist (non-key columns should not depend on other non-key columns).

    **Problem**: The `manager` column depends on `department`, not the primary key (`emp_id`).

    **Solution**: Separate `manager` into its own table linked to `department`.
    """)

    employee_table = pd.DataFrame({
        'emp_id': [1, 2, 3, 4],
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'department': ['HR', 'Engineering', 'Engineering', 'Marketing']
    })

    manager_table = pd.DataFrame({
        'department': ['HR', 'Engineering', 'Marketing'],
        'manager': ['Eve', 'Tom', 'Susan']
    })

    st.subheader("Employee Table")
    st.dataframe(employee_table)

    st.subheader("Manager Table")
    st.dataframe(manager_table)

    sql_command = """
    CREATE TABLE employees (
        emp_id INT PRIMARY KEY,
        name VARCHAR(50),
        department VARCHAR(50)
    );

    CREATE TABLE managers (
        department VARCHAR(50),
        manager VARCHAR(50)
    );
    """
    st.markdown("**SQL Queries to Normalize to 3NF:**")
    st.code(sql_command, language="sql")

# Boyce-Codd Normal Form (BCNF)
with tabs[3]:
    st.header("🔹 Boyce-Codd Normal Form (BCNF)")
    st.markdown("""
    **Definition**: A table is in BCNF if:
    - It is in 3NF.
    - Every determinant is a candidate key.

    **Problem Example**:
    - A table with columns (`student_id`, `course`, `instructor`) where:
      - `course → instructor`
      - `student_id, course` is the primary key.

    **Solution**:
    - Decompose into two tables: one for courses and instructors, and one for student-course relationships.
    """)

    course_table = pd.DataFrame({
        'course': ['Math', 'Science', 'History'],
        'instructor': ['Dr. Smith', 'Dr. Brown', 'Dr. Johnson']
    })

    enrollment_table = pd.DataFrame({
        'student_id': [1, 2, 3],
        'course': ['Math', 'Science', 'History']
    })

    st.subheader("Course Table")
    st.dataframe(course_table)

    st.subheader("Enrollment Table")
    st.dataframe(enrollment_table)

    sql_command = """
    CREATE TABLE courses (
        course VARCHAR(50) PRIMARY KEY,
        instructor VARCHAR(50)
    );

    CREATE TABLE enrollments (
        student_id INT,
        course VARCHAR(50),
        FOREIGN KEY (course) REFERENCES courses(course)
    );
    """
    st.markdown("**SQL Queries for BCNF:**")
    st.code(sql_command, language="sql")

# Denormalization Techniques
with tabs[4]:
    st.header("🔄 Denormalization Techniques")
    st.markdown("""
    **Definition**: Denormalization combines normalized tables to reduce the number of joins required for queries.

    While normalization reduces redundancy, denormalization optimizes query performance by reintroducing some redundancy. This is often done in scenarios where read performance is more critical than write performance.

    **Common Techniques**:
    1. **Merging Tables**: Combine related tables into one.
    2. **Adding Redundant Data**: Include data from related tables to avoid joins.
    3. **Storing Computed Values**: Save aggregated or calculated values to reduce on-the-fly computations.
    """)

    sql_command = """
    SELECT e.emp_id, e.name, e.department, m.manager
    FROM employees e
    JOIN managers m ON e.department = m.department;
    """
    st.markdown("**SQL Query to Create a Denormalized Table:**")
    st.code(sql_command, language="sql")


# Benefits & Trade-offs
with tabs[5]:
    st.header("⚖️ Benefits & Trade-offs")
    st.markdown("""
    **Normalization vs. Denormalization**

    | Aspect                    | Normalization                                    | Denormalization                               |
    |---------------------------|-------------------------------------------------|---------------------------------------------|
    | **Purpose**               | Minimize redundancy and maintain integrity      | Optimize read/query performance             |
    | **Data Redundancy**       | Eliminated                                     | Reintroduced                                 |
    | **Query Complexity**      | More complex (requires joins)                  | Simpler (fewer joins)                       |
    | **Write Performance**     | Faster (less duplication to maintain)          | Slower (more updates due to redundancy)     |
    | **Read Performance**      | Slower (requires joins)                        | Faster (joins minimized)                    |
    | **Use Case**              | Transactional systems                          | Analytical systems, reporting               |

    ### Benefits of Normalization:
    - Reduces data redundancy and ensures consistency.
    - Saves storage space.
    - Maintains data integrity during updates.

    ### Benefits of Denormalization:
    - Improves query performance for read-heavy systems.
    - Reduces the need for complex joins.

    ### Trade-offs:
    - Normalization increases query complexity and join operations.
    - Denormalization introduces redundancy and potential for inconsistencies.
    """)

    st.markdown("### Interactive Comparison")
    st.markdown("Choose a scenario to see whether normalization or denormalization is better suited:")
    scenario = st.selectbox(
        "Select a Scenario:",
        ["Transaction Processing (e.g., Banking System)", "Data Analysis (e.g., Reporting Dashboard)"]
    )

    if scenario == "Transaction Processing (e.g., Banking System)":
        st.success("✅ Normalization is preferred to ensure data consistency and integrity in write-heavy systems.")
    elif scenario == "Data Analysis (e.g., Reporting Dashboard)":
        st.success("✅ Denormalization is better for read-heavy systems like dashboards to speed up queries.")

# Footer Quiz Section
st.markdown("---")
st.header("🎯 Test Your Knowledge!")
quiz_question = st.multiselect(
    "Which of the following are advantages of normalization? (Select all that apply)",
    [
        "Minimizes data redundancy",
        "Improves query performance in read-heavy systems",
        "Ensures data consistency",
        "Simplifies queries"
    ],
    key="quiz_normalization"
)

if st.button("Submit Answer", key="quiz_submit_denormalization"):
    correct_answers = {"Minimizes data redundancy", "Ensures data consistency"}
    selected_answers = set(quiz_question)

    if selected_answers == correct_answers:
        st.success("Correct! 🎉 Normalization minimizes redundancy and ensures data consistency.")
    else:
        missing_answers = correct_answers - selected_answers
        extra_answers = selected_answers - correct_answers

        feedback = "Oops! Here's what you got wrong:\n"
        if missing_answers:
            feedback += f"- Missing correct answer(s): {', '.join(missing_answers)}\n"
        if extra_answers:
            feedback += f"- Incorrect answer(s): {', '.join(extra_answers)}\n"
        st.error(feedback)

# Footer Quiz Section
st.markdown("---")
quiz_question = st.multiselect(
    "Which normalization form ensures no partial dependency?",
    ["1NF", "2NF", "3NF", "BCNF"],
    key="normalization_quiz"
)

if st.button("Submit Answer", key="quiz_submit"):
    correct_answers = {"2NF"}
    selected_answers = set(quiz_question)
    if selected_answers == correct_answers:
        st.success("Correct! 🎉 2NF removes partial dependencies.")
    else:
        st.error(f"Incorrect! The correct answer is 2NF.")

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