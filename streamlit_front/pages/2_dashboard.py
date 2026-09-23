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
    

@st.cache_data(show_spinner="Fetching data from API...")
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

if 'symbols_filter' not in st.session_state:
     st.session_state.symbols_filter = ['btc', 'eth', 'usdt', 'sol']
def update_linear_graph():
    pass

with st.sidebar:
    st.sidebar.header("Dashboard V1")
    st.multiselect('Select the crypto you want to visualize', 
                options= params['symbol'],
                key='symbols_filter')

st.set_page_config(page_title="Dashboard", page_icon="📊")
st.title("Crypto dashboard")
with st.container(border=True):
   
    st.markdown("## Dashboard V1")
    st.write(
        """Testing the api call"""
    )
        
with st.expander("Complete dataframe"):
    df = get_api_data(url, params, headers)
    st.write(df)

"---"
fig = px.line(df, x='bucket', y='avg_price', title='Crypto', color='symbol')
st.plotly_chart(fig)


    

# st.write(st.session_state.symbols_filter)

# params = { 
#         'symbol': 'btc', 'eth', 'usdt', 'sol'
#         'duration': '1 hour',
#         'history': '7 days'
# }         





st.title('Counter Example')
if 'count' not in st.session_state:
    st.session_state.count = 0
    st.session_state.last_updated = datetime.time(0,0)

def update_counter():
    st.session_state.count += st.session_state.increment_value
    st.session_state.last_updated = st.session_state.update_time

with st.form(key='my_form'):
    st.time_input(label='Enter the time', value=datetime.datetime.now().time(), key='update_time')
    st.number_input('Enter a value', value=0, step=1, key='increment_value')
    submit = st.form_submit_button(label='Update', on_click=update_counter)

st.write('Current Count = ', st.session_state.count)
st.write('Last Updated = ', st.session_state.last_updated)