import streamlit as st


main_page = st.Page("pages/1_home.py", title="Main", icon="🎈")
page_2 = st.Page("pages/2_dashboard.py", title="Dashboard", icon="❄️")
#page_3 = st.Page("pages/3_AI.py", title="Page 3", icon="🤖")



# Set up navigation
pg = st.navigation([main_page, page_2])

# Run the selected page
pg.run()


