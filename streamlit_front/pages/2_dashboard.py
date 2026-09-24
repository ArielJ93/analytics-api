import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import datetime

st.set_page_config(page_title="Dashboard", page_icon="📊")

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

@st.cache_data(show_spinner=False, ttl=900)
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
    


with st.sidebar:
    st.sidebar.header("Dashboard V1")
    selection_mode = st.radio("Crypto selection", options=["One coin", "Multiple coins"])
    if selection_mode == "One coin":
        symbol_filter = st.multiselect('Select the crypto you want to visualize:', 
                options= params['symbol'],
                default= ['btc'],
                max_selections=1)
    if selection_mode == "Multiple coins":
        symbol_filter = st.multiselect('Select cryptos to compare:', 
                    options= params['symbol'],
                    default= ['m', 'dot', 'render', 'atom'])
    st.divider()
    duration_filter = st.pills("Select the interval values:", options=["15 minutes","1 hour", "4 hours", "1 day"], default= "15 minutes")
    st.divider()
    history_filter = st.pills("Select the date of all the data you want to fecth:", options=["1 day","7 days", "30 days"], default= "1 day")


filter_params = { 
        'symbol': symbol_filter,
        
        'duration': duration_filter,
        
        'history': history_filter
}


st.title("Crypto dashboard", anchor=False)

if not symbol_filter:
    with st.container(border=True):
        st.warning("⚠️ **Please select at least one cryptocurrency in the sidebar to visualize the data.**")
else:
    with st.container(border=True):   
        with st.spinner("Fetching data from API...", show_time=True):
            df = get_api_data(url, filter_params, headers) 
            if len(symbol_filter) == 1:
                metric_1, metric_2, metric_3 = st.columns(3)
                with metric_1:
                    #delta is the percentage change between the first row  and the last row, the time interval between the first row and the last one represent the interval selected on the history filter.
                    delta_price = ((df['avg_price'].iloc[-1] - df['avg_price'].iloc[1]) / df['avg_price'].iloc[1]) * 100
                    st.metric("PRICE  $USD", value=df['avg_price'].iloc[-1], delta=f"{delta_price:.2f}%")
                with metric_2:
                    delta_volume = ((df['volume_24h'].iloc[-1] - df['volume_24h'].iloc[1]) / df['volume_24h'].iloc[1]) * 100
                    st.metric("VOLUME 24H", value=df['volume_24h'].iloc[-1], delta=f"{delta_volume:.2f}%")
                with metric_3:
                    delta_market = ((df['market_cap'].iloc[-1] - df['market_cap'].iloc[1]) / df['market_cap'].iloc[1]) * 100
                    st.metric("MARKET CAP", value=df['market_cap'].iloc[-1], delta=f"{delta_market:.2f}%")
                
            line_graph_tab, bubble_chart, heat_map, df_tab = st.tabs(["Linear Graph", "Bubble Chart", "Heat Map", "Complete DataFrame"])
            with line_graph_tab:
                fig = px.line(df, x='bucket', y='avg_price', color='symbol')
                fig.update_layout(
                    title={
                        'text': 'Average Price over time',
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'},
                    xaxis=dict(
                        title=dict(
                            text="Time"
                                        )),
                    yaxis=dict(
                        title=dict(
                            text="Price $USD"
                                )))
                st.plotly_chart(fig)
            if len(symbol_filter) > 1:
                with bubble_chart:
                    animation = st.checkbox(label="Animation of data history")
                    if animation:
                        fig = px.scatter(
                                    df, x="change_24h", y="volume_24h",
                                    size="market_cap", color="symbol",
                                    hover_name="symbol",
                                    log_y=True,
                                    size_max=60,
                                    animation_frame="bucket",
                                    animation_group="symbol")
                        fig.update_layout(
                            title={
                                'text': 'Volume vs Percentual Change (24h)',
                                'y':0.9,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'})
                        st.plotly_chart(fig)
                    else:
                        last_date = df['bucket'].iloc[-1]
                        df_bubble_chart = df[df['bucket'] == last_date]
                        fig = px.scatter(df_bubble_chart, x="change_24h", y="volume_24h",
                                size="market_cap", color="symbol",
                                hover_name="symbol",
                                log_y=True,
                                size_max=60,
                                )
                        fig.update_layout(
                            title={
                                'text': 'Volume vs Percentual Change (24h) <br><sup>*Bubble size represents Market Cap</sup>',
                                'y':0.9,
                                'x':0.5,
                                'xanchor': 'center',
                                'yanchor': 'top'})
                        st.plotly_chart(fig)
            with df_tab:
                st.dataframe(df)
        
