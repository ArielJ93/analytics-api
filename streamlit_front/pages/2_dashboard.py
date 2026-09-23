import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import datetime


base_url = "https://analytics-api-hg65.onrender.com"
path = "/api/v1/analytics"
url = f"{base_url}{path}"
headers = {
    "content-type": "application/json"
}
params = { 
        'symbol': ['btc', 'eth', 'usdt', 'bnb', 'xrp', 'usdc', 'sol', 'trx', 'zec', 'hype', 'doge', 'xmr', 'wbt', 'rain', 'link','usds', 'ada', 'leo', 'xlm', 'near', 'uni', 'bch', 'usde', 'avax', 'ltc', 'cc', 'dai', 'usd1', 'sui', 'hbar', 'gram', 'shib','tao', 'cro', 'usdg', 'm', 'pyusd', 'xaut', 'okb', 'usyc', 'rlusd', 'buidl', 'btw', 'usdy', 'aave', 'pepe', 'ondo', 'ena', 'mnt', 'pump', 'dot', 'aster', 'paxg', 'wlfi', 'morpho', 'wld', 'icp', 'sky', 'htx', 'usdd', 'arb', 'vvv', 'bgb', 'eursafo', 'u', 'usdgo', 'etc', 'usdf', 'bfusd', 'ake', 'kas', 'pol', 'lit', 'gt', 'pi', 'algo', 'kcs', 'jup', 'bcap', 'qnt', 'atom', 'render', 'jst', 'nexo', 'fil', 'cake', 'eutbl', 'jaaa', 'dash', 'vet', 'inj', 'ustb', 'gho', 'aero', 'ethfi', 'apt', 'stable', 'stx', 'xdc'],
        
        'duration': '1 hour',
        
        'history': '7 days'
}

    
@st.cache_data(show_spinner=False)
def get_api_data(url, params, headers):
    try:
        response = requests.get(url=url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        data = pd.DataFrame(data)
        return data
    except Exception as e:
        st.error(f"API error conexion: {e}")
        return None

# if 'symbols_filter' not in st.session_state:
#      st.session_state.symbols_filter = ['btc', 'eth', 'usdt', 'sol']
# if 'duration_filter' not in st.session_state:
#     st.session_state.duration_filter = "15 minutes"
# if 'history_filter' not in st.session_state:
#     st.session_state.history_filter = "1 day"
    
def graph_callback():
    pass

with st.sidebar:
    st.sidebar.header("Dashboard V1")
    symbol_filter = st.multiselect('Select the crypto you want to visualize:', 
                options= params['symbol'],
                default= ['btc', 'eth', 'usdt', 'sol'])
    st.divider()
    duration_filter = st.pills("Select the interval values:", options=["15 minutes","1 hour", "4 hours", "1 day"], default= "15 minutes")
    st.divider()
    history_filter = st.pills("Select the date of all the data you want to fecth:", options=["1 day","7 days", "30 days"], default= "1 day")


filter_params = { 
        'symbol': symbol_filter,
        
        'duration': duration_filter,
        
        'history': history_filter
}

st.set_page_config(page_title="Dashboard", page_icon="📊")
st.title("Crypto dashboard")

with st.container(border=True):
   
    st.markdown("## Dashboard V1")
    st.write(
        """Testing the api call"""
    )

with st.container(border=True):   
    with st.spinner("Fetching data from API...", show_time=True):
        df = get_api_data(url, filter_params, headers)    
        line_graph_tab, df_tab = st.tabs(["Linear Graph", "Complete DataFrame"])
        with line_graph_tab:
            fig = px.line(df, x='bucket', y='avg_price', title='Crypto', color='symbol')
            st.plotly_chart(fig)
        with df_tab:
            st.dataframe(df)

