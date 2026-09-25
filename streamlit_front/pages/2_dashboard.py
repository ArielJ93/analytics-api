import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

base_url = "https://analytics-api-hg65.onrender.com"
path = "/api/v1/analytics"
url = f"{base_url}{path}"
headers = {
    "content-type": "application/json"
}

all_symbols = ['btc', 'eth', 'usdt', 'bnb', 'xrp', 'usdc', 'sol', 'trx', 'zec', 'hype', 'doge', 'xmr', 'wbt', 'rain', 'link','usds', 'ada', 'leo', 'xlm', 'near', 'uni', 'bch', 'usde', 'avax', 'ltc', 'cc', 'dai', 'usd1', 'sui', 'hbar', 'gram', 'shib','tao', 'cro', 'usdg', 'm', 'pyusd', 'xaut', 'okb', 'usyc', 'rlusd', 'buidl', 'btw', 'usdy', 'aave', 'pepe', 'ondo', 'ena', 'mnt', 'pump', 'dot', 'aster', 'paxg', 'wlfi', 'morpho', 'wld', 'icp', 'sky', 'htx', 'usdd', 'arb', 'vvv', 'bgb', 'eursafo', 'u', 'usdgo', 'etc', 'usdf', 'bfusd', 'ake', 'kas', 'pol', 'lit', 'gt', 'pi', 'algo', 'kcs', 'jup', 'bcap', 'qnt', 'atom', 'render', 'jst', 'nexo', 'fil', 'cake', 'eutbl', 'jaaa', 'dash', 'vet', 'inj', 'ustb', 'gho', 'aero', 'ethfi', 'apt', 'stable', 'stx', 'xdc']


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

with st.sidebar:
    st.title("Global filters")
    with st.container():
        duration_filter = st.pills("Select the interval values:", options=["15 minutes","1 hour", "4 hours", "1 day"], default= "15 minutes")
        st.divider()
        history_filter = st.pills("Select the date of all the data you want to fecth:", options=["1 day","7 days", "30 days"], default= "1 day")


st.title("Crypto dashboard", anchor=False)

with st.container(border=True):      

    line_graph_tab, bubble_chart, tree_map, df_tab = st.tabs(["Price Evolution", "Market Dynamics", "Dominance Map", "Data Table"])
    
    with line_graph_tab:
        symbol_filter = st.selectbox('Select crypto coin:', 
        options= all_symbols,
        index= 0)
        filter_params = { 
                'symbol': symbol_filter,
                
                'duration': duration_filter,
                
                'history': history_filter
        }
        if not symbol_filter:
                st.warning("⚠️ **select at least one cryptocurrency to visualize the data.**")
        else:
            with st.spinner("Fetching data from API...", show_time=True): 
                df = get_api_data(url, filter_params, headers)
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
            fig = px.line(df, x='bucket', y='avg_price', color='symbol')
            fig.update_layout(
                title={
                    'text': 'Average Price over time',
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'},
                xaxis=dict(title=dict(text="Time")),
                yaxis=dict(title=dict(text="Price $USD"))
                )
            st.plotly_chart(fig, width='stretch')
            
    with bubble_chart:
        bubble_filter = st.multiselect(label="Select crypto coin/s", options=all_symbols, max_selections=10, default=all_symbols[:5])
        bubble_params = { 
                'symbol': bubble_filter,
                
                'duration': duration_filter,
                
                'history': history_filter
        }
        if not bubble_filter:
                st.warning("⚠️ **select at least one cryptocurrency to visualize the data.**")
        else:
            with st.spinner("Fetching data from API...", show_time=True): 
                df = get_api_data(url, bubble_params, headers)
            animation = st.checkbox(label="Animation of data history")
            if animation:
                with st.spinner("Loading animated bubble chart...", show_time=True):
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
                            'text': 'Data history animation of Volume vs Percentual Change (24h) <br><sup>*Bubble size represents Market Cap</sup>',
                            'y':0.9,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'},
                            xaxis_ticksuffix="%")
                    fig.update_yaxes(tickformat="$~s")
                    st.plotly_chart(fig, width='stretch')
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
                        'yanchor': 'top'},
                        xaxis_ticksuffix="%")
                fig.update_yaxes(tickformat="$~s")
                st.plotly_chart(fig, width='stretch')
                
    with tree_map:
        filter_params = { 
                'symbol': all_symbols,
                
                'duration': duration_filter,
                
                'history': history_filter
        }
        with st.spinner("Fetching data from API...", show_time=True): 
            df = get_api_data(url, filter_params, headers)
        last_date = df['bucket'].iloc[-1]
        date = datetime.fromisoformat(last_date)
        date_formated = date.strftime("%d/%m/%Y")
        st.subheader(f"Market Cap of the top 100 coins\nDate: {date_formated}")
        fig = px.treemap(
            df, 
            path=["symbol"], 
            values="market_cap", 
            color="change_24h", 
            color_continuous_scale='RdBu')
        fig.update_traces(root_color="lightgrey")
        fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
        st.plotly_chart(fig, width='stretch')
        
    with df_tab:
        st.dataframe(df)

