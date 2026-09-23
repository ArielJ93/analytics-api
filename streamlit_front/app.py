import streamlit as st


main_page = st.Page("pages/1_home.py", title="Hello", icon="🎈")
page_2 = st.Page("pages/2_dashboard.py", title="Page 2", icon="❄️")
page_3 = st.Page("pages/3_AI.py", title="Page 3", icon="🤖")
page_4 = st.Page("pages/4_feedback.py", title="Page 4", icon="🎉")


# Set up navigation
pg = st.navigation([main_page, page_2, page_3, page_4])

# Run the selected page
pg.run()


