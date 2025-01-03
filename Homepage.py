import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Interactive SQL Learning Platform",
    page_icon="📊",
    layout="wide"
)

# Title and Subtitle
st.title("📊 SQL")
st.markdown("""
Welcome to the **Interactive SQL Learning Platform**! 🎉  
This platform is designed to make learning SQL fun, engaging, and hands-on. Whether you're a beginner or an experienced user, there's something here for everyone! 🚀
""")

# Main Sections
st.markdown("---")
st.header("✨ What You’ll Learn:")
st.markdown("""
- **Basics of SQL**: Understand fundamental concepts like `SELECT`, `WHERE`, and `JOIN`.
- **Intermediate Topics**: Dive into `GROUP BY`, `HAVING`, subqueries, and set operations.
- **Advanced Concepts**: Explore CTEs, window functions, recursive queries, and performance tuning.
- **Practical Applications**: Learn how to optimize queries, work with triggers, transactions, and more!
""")


# Quiz Teaser
st.markdown("---")
st.header("🎯 Ready for a Challenge?")
st.markdown("""
Test your knowledge with interactive quizzes after each section.  
Track your progress and improve as you go! 🌟
""")

if st.button("Start Learning Now! 🚀"):
    st.success("Great! Navigate to the topics on the left sidebar to begin your journey.")

# Footer Section
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin-top: 20px;">
    Made with ❤️ by 
    <a href="mailto:riyabasu06@gmail.com" style="text-decoration: none; color: #2e77d0;">
        <strong>Riya Bose</strong>
    </a>
</div>
""", unsafe_allow_html=True)
