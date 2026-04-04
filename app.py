"""
Economic Outlook Dashboard
Live tracking of global economic indicators with auto-refresh
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from PIL import Image

# Import our data modules
from data_sources import (
    fetch_all_live_data, get_current_snapshot,
    get_gdp_growth, get_cpi_inflation, get_unemployment_rate,
    get_treasury_yields, get_stock_indices, get_oil_prices,
    get_currency_rates, get_global_bond_yields, get_crypto_prices
)
from config import (
    REFRESH_INTERVALS, AUTO_REFRESH_ENABLED, AUTO_REFRESH_DEFAULT,
    CHART_COLORS, REGION_METRICS, THEME
)

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Economic Outlook Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Report': 'Global Economic Outlook Dashboard',
        'Go to homepage': "https://google.com",
        'About': "📊 Live Economic Dashboard\n\nTrack real-time economic indicators across global regions including GDP, inflation, unemployment, bond yields, stock markets, and currencies.\n\n🔄 Auto-refresh enabled\n📈 Interactive charts and tables\n⚡ Powered by free public APIs",
    }
)

# Apply custom CSS
st.markdown("""
<style>
    .stMetric {font-size: 1.5rem; font-weight: bold;}
    .region-card {padding: 1rem; border-radius: 8px; margin-bottom: 1rem;}
    .metric-value {font-size: 1.8rem; font-weight: 700;}
    .metric-label {font-size: 0.9rem; opacity: 0.8;}
    .data-updated {text-align: center; color: #666; font-size: 0.85rem; margin-top: 1rem;}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# INITIALIZATION
# =============================================================================

@st.cache_data(ttl=3600)
def get_cached_data():
    """Get cached economic data"""
    print("Loading cached data...")
    data = fetch_all_live_data()
    return data


def get_latest_date(data):
    """Get latest data date"""
    try:
        return data['10y_yield'].index[-1].strftime('%Y-%m-%d %H:%M')
    except:
        return "Unknown"


# =============================================================================
# SIDEBAR CONTROLS
# =============================================================================

st.sidebar.header("⚙️ Settings")

# Auto-refresh control
auto_refresh = st.sidebar.checkbox("Enable Auto-Refresh", value=AUTO_REFRESH_ENABLED)
if auto_refresh:
    refresh_interval = st.sidebar.select_slider(
        "Refresh Interval",
        options=['5 min', '10 min', '15 min', '30 min', '1 hour', '2 hours'],
        format="%H:%M",
        value="30 min" if AUTO_REFRESH_DEFAULT == 3600 else "10 min"
    )
    # Convert to seconds
    interval_map = {'5 min': 300, '10 min': 600, '15 min': 900, '30 min': 1800, '1 hour': 3600, '2 hours': 7200}
    REFRESH_INTERVALS['default'] = interval_map[refresh_interval]
else:
    refresh_interval = "Manual"

# Chart settings
chart_size = st.sidebar.selectbox("Chart Size", ["Small", "Medium", "Large"])
chart_sizes = {
    "Small": (400, 300),
    "Medium": (600, 400),
    "Large": (800, 500)
}

# Data source toggle (for testing)
use_hardcoded_data = st.sidebar.checkbox("Use NotebookLM Sample Data", value=False)

# =============================================================================
# DATA FETCHING
# =============================================================================

if use_hardcoded_data:
    print("Using NotebookLM sample data...")
    # Create simulated data based on NotebookLM research
    data = {
        'gdp': {
            'US': pd.Series(np.array([2.5, 2.3, 2.0, 2.5, 1.7, 1.7, 1.8, 1.9, 2.0, 2.1]) +
                           np.random.normal(0, 0.2, 50)),
            'Eurozone': pd.Series(np.array([0.2, 0.0, -0.3, 0.1, 0.0, 0.2, 0.0, 0.1, 0.0, 0.2]) +
                                np.random.normal(0, 0.1, 50)),
            'China': pd.Series(np.array([5.0, 4.9, 5.2, 4.8, 5.0, 5.2, 5.0, 5.1, 4.9, 5.0]) +
                              np.random.normal(0, 0.1, 50)),
            'Japan': pd.Series(np.array([0.3, 0.2, 0.4, 0.1, 0.2, 0.3, 0.2, 0.3, 0.1, 0.2]) +
                              np.random.normal(0, 0.1, 50)),
            'UK': pd.Series(np.array([0.3, 0.5, 0.2, 0.1, 0.0, 0.2, 0.1, 0.3, 0.2, 0.2]) +
                           np.random.normal(0, 0.1, 50)),
            'EM': pd.Series(np.array([4.5, 5.0, 3.5, 3.0, 2.5, 3.0, 4.0, 3.5, 4.5, 5.0]) +
                           np.random.normal(0, 0.5, 50)),
        },
        'inflation': {
            'US': pd.Series(np.array([3.0, 3.1, 3.2, 3.0, 3.1, 3.0, 2.9, 2.8, 2.9, 3.0]) +
                           np.random.normal(0, 0.2, 50)),
            'Eurozone': pd.Series(np.array([2.4, 2.5, 2.6, 2.4, 2.5, 2.4, 2.6, 2.5, 2.4, 2.3]) +
                                np.random.normal(0, 0.15, 50)),
            'China': pd.Series(np.array([1.5, 1.2, 1.0, 0.8, 0.9, 1.0, 0.9, 1.1, 1.0, 1.2]) +
                              np.random.normal(0, 0.1, 50)),
            'Japan': pd.Series(np.array([0.3, 0.5, 0.2, 0.1, 0.0, 0.2, 0.1, 0.3, 0.2, 0.3]) +
                              np.random.normal(0, 0.1, 50)),
            'UK': pd.Series(np.array([2.3, 2.5, 3.0, 2.8, 2.6, 2.4, 2.3, 2.5, 2.4, 2.3]) +
                           np.random.normal(0, 0.2, 50)),
        },
        '10y_yield': pd.Series(np.array([3.8, 3.9, 4.0, 4.1, 3.9, 4.0, 4.1, 4.2, 4.0, 3.9]) +
                               np.random.normal(0, 0.1, 50)),
        'sp500': pd.Series(np.array([4200, 4250, 4300, 4350, 4400, 4350, 4400, 4450, 4500, 4550]) +
                          np.random.normal(0, 20, 50)),
        'oil': pd.Series(np.array([78, 82, 88, 92, 105, 108, 110, 105, 98, 92]) +
                        np.random.normal(0, 3, 50)),
        'currencies': {
            'EUR/USD': pd.Series(np.array([1.08, 1.09, 1.07, 1.06, 1.05, 1.06, 1.07, 1.06, 1.05, 1.04]) +
                                np.random.normal(0, 0.01, 50)),
            'GBP/USD': pd.Series(np.array([1.25, 1.27, 1.24, 1.22, 1.20, 1.21, 1.22, 1.21, 1.20, 1.19]) +
                               np.random.normal(0, 0.01, 50)),
            'USD/JPY': pd.Series(np.array([150, 148, 152, 150, 148, 149, 151, 149, 148, 147]) +
                               np.random.normal(0, 1, 50)),
            'USD/CNY': pd.Series(np.array([7.20, 7.22, 7.25, 7.28, 7.30, 7.28, 7.30, 7.28, 7.26, 7.24]) +
                               np.random.normal(0, 0.02, 50)),
            'USD/INR': pd.Series(np.array([83.0, 83.5, 84.0, 83.8, 83.5, 83.2, 83.0, 83.3, 83.0, 82.8]) +
                               np.random.normal(0, 0.3, 50)),
        },
        'crypto': {
            'Bitcoin': pd.Series(np.array([64000, 65000, 66000, 67000, 66500, 67000, 68000, 69000, 70000, 71000]) +
                                np.random.normal(0, 500, 50)),
            'Ethereum': pd.Series(np.array([3000, 3050, 3100, 3150, 3200, 3150, 3200, 3250, 3300, 3350]) +
                                np.random.normal(0, 50, 50)),
        },
    }

    # Update GDP with actual dates
    dates = pd.date_range(end=datetime.now(), periods=50, freq='M')
    for region in data['gdp']:
        data['gdp'][region].index = dates

    # Update inflation with actual dates
    for region in data['inflation']:
        data['inflation'][region].index = dates

    # Update 10y yield
    data['10y_yield'].index = dates

    # Update stocks
    data['sp500'].index = dates

    # Update oil
    data['oil'].index = dates

    # Update currencies
    for pair in data['currencies']:
        data['currencies'][pair].index = dates

    # Update crypto
    for coin in data['crypto']:
        data['crypto'][coin].index = dates

    # Get current snapshot
    current = {
        'US_GDP': round(data['gdp']['US'].iloc[-1], 1),
        'EU_GDP': round(data['gdp']['Eurozone'].iloc[-1], 1),
        'CN_GDP': round(data['gdp']['China'].iloc[-1], 1),
        'JP_GDP': round(data['gdp']['Japan'].iloc[-1], 1),
        'UK_GDP': round(data['gdp']['UK'].iloc[-1], 1),
        'EM_GDP': round(data['gdp']['EM'].iloc[-1], 1),
        'US_Inflation': round(data['inflation']['US'].iloc[-1], 1),
        'EU_Inflation': round(data['inflation']['Eurozone'].iloc[-1], 1),
        'CN_Inflation': round(data['inflation']['China'].iloc[-1], 1),
        'JP_Inflation': round(data['inflation']['Japan'].iloc[-1], 1),
        'UK_Inflation': round(data['inflation']['UK'].iloc[-1], 1),
        '10Y_Yield': round(data['10y_yield'].iloc[-1], 2),
        'SP500': round(data['sp500'].iloc[-1], 0),
        'Oil_WTI': round(data['oil'].iloc[-1], 0),
        'EURUSD': round(data['currencies']['EUR/USD'].iloc[-1], 2),
        'BTC': round(data['crypto']['Bitcoin'].iloc[-1], 0),
    }
else:
    data = get_cached_data()
    current = get_current_snapshot()


def get_latest_value(series):
    """Get latest value from a series"""
    try:
        if not series.empty:
            return round(series.iloc[-1], 2)
    except:
        pass
    return None


# =============================================================================
# UPDATE INDICATOR (for auto-refresh)
# =============================================================================

def update_data():
    """Update data with new values"""
    if auto_refresh:
        try:
            # Fetch fresh oil prices (most volatile)
            oil_data = get_oil_prices()
            if oil_data['WTI'] is not None and not oil_data['WTI'].empty:
                data['oil'] = oil_data['WTI']
            if oil_data['Brent'] is not None and not oil_data['Brent'].empty:
                data['oil'] = oil_data['Brent']

            # Fetch fresh treasury yields (daily)
            yields = get_treasury_yields()
            for yield_name, yield_series in yields.items():
                if yield_series is not None and not yield_series.empty:
                    data['treasury'][yield_name] = yield_series
            data['10y_yield'] = yields.get('DGS10', data['10y_yield'])

            # Fetch fresh stock indices (daily)
            indices = get_stock_indices()
            for name, series in indices.items():
                if series is not None and not series.empty:
                    data['indices'][name] = series

        except Exception as e:
            print(f"Update error: {e}")


# Run update if auto-refresh is on (throttled)
if auto_refresh:
    # Check if oil needs update (every 5 minutes)
    if data['oil'].empty or (datetime.now() - data['oil'].index[-1]).seconds > 300:
        update_data()
    # Check if yields need update (every hour)
    if data['10y_yield'].empty or (datetime.now() - data['10y_yield'].index[-1]).seconds > 3600:
        update_data()
    # Check if stocks need update (daily)
    if data['sp500'].empty or (datetime.now() - data['sp500'].index[-1]).days > 0:
        update_data()

# Get current timestamp
latest_date = get_latest_date(data)

# =============================================================================
# HEADER
# =============================================================================

st.title("📊 Economic Outlook Dashboard")
st.markdown(f"**Latest Update:** {latest_date}")

# =============================================================================
# GLOBAL SUMMARY METRICS
# =============================================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Oil Price
    oil_price = get_latest_value(data['oil'])
    if oil_price:
        st.metric(label="🛢️ Oil (Brent)", value=f"${oil_price}", delta=f"~$110 (current)")
    else:
        st.metric(label="🛢️ Oil (Brent)", value="N/A")

with col2:
    # US Dollar Index
    try:
        dxy = get_stock_indices().get('US Dollar', pd.Series())
        if not dxy.empty:
            dxy_latest = round(dxy.iloc[-1], 2)
            st.metric(label="🇺🇸 USD Index", value=f"{dxy_latest}", delta="+/- 0.1%")
    except:
        pass

with col3:
    # Gold Price
    try:
        gold = get_crypto_prices().get('Gold', pd.Series())
        if not gold.empty:
            gold_latest = round(gold.iloc[-1], 0)
            st.metric(label="🥇 Gold", value=f"${gold_latest}", delta="+/- 1%")
    except:
        pass

with col4:
    # Crypto (Bitcoin)
    btc = get_latest_value(data['crypto']['Bitcoin'])
    if btc:
        st.metric(label="₿ Bitcoin", value=f"${btc}", delta="+/- 3%")
    else:
        st.metric(label="₿ Bitcoin", value="N/A")

# =============================================================================
# REGION CARDS
# =============================================================================

st.subheader("🌍 Regional Economic Overview")

regions = ['US', 'Eurozone', 'China', 'Japan', 'UK', 'Emerging Markets']
region_labels = ['United States', 'Eurozone', 'China', 'Japan', 'United Kingdom', 'Emerging Markets']

for i, region in enumerate(regions):
    col = st.columns(2)[i % 2]
    with col:
        # Create colored card
        color = CHART_COLORS[region]
        card_html = f"""
        <div class="region-card" style="
            background: linear-gradient(135deg, {color['primary']} 0%, {color['secondary']} 100%);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.5rem;">
            <h4 style="margin: 0 0 0.5rem 0;">{region_labels[i]} ({region})</h4>
            <div style="font-size: 2.5rem; font-weight: bold;">
                {get_latest_value(data['gdp'][region]) or 'N/A'}%
            </div>
            <div style="font-size: 0.8rem; opacity: 0.9;">GDP Growth (YoY)</div>
            <hr style="border-color: rgba(255,255,255,0.3); margin: 0.5rem 0;">
            <div style="font-size: 1.2rem; font-weight: bold;">
                {get_latest_value(data['inflation'][region]) or 'N/A'}%
            </div>
            <div style="font-size: 0.8rem; opacity: 0.9;">Inflation</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# =============================================================================
# MAIN CHARTS SECTION
# ======================================================================

st.subheader("📈 Economic Trends")

# Chart 1: GDP Growth Comparison
st.markdown("### GDP Growth Comparison")
gdp_comparison = {}
for region in regions:
    series = data['gdp'][region]
    if series is not None and not series.empty:
        gdp_comparison[region_labels[regions.index(region)]] = series

if gdp_comparison:
    fig_gdp = go.Figure()
    for region, series in gdp_comparison.items():
        fig_gdp.add_trace(go.Scatter(
            x=series.index,
            y=series,
            mode='lines+markers',
            name=region[:3],
            line=dict(color=CHART_COLORS[region]['primary'], width=2),
            marker=dict(size=6)
        ))
    fig_gdp.update_layout(
        title="GDP Growth Rate Comparison",
        xaxis_title="Date",
        yaxis_title="Growth Rate (%)",
        height=400,
        hovermode='x unified',
        xaxis=dict(tickangle=45)
    )
    st.plotly_chart(fig_gdp, use_container_width=True)

# Chart 2: Inflation Trends
st.markdown("### Inflation Trends")
inf_comparison = {}
for region in regions[:5]:  # Only 5 regions with inflation data
    series = data['inflation'][region]
    if series is not None and not series.empty:
        inf_comparison[region_labels[regions.index(region)]] = series

if inf_comparison:
    fig_inf = go.Figure()
    for region, series in inf_comparison.items():
        fig_inf.add_trace(go.Scatter(
            x=series.index,
            y=series,
            mode='lines+markers',
            name=region[:3],
            line=dict(color=CHART_COLORS[region]['primary'], width=2)
        ))
    fig_inf.update_layout(
        title="Inflation Rate Trends",
        xaxis_title="Date",
        yaxis_title="Inflation Rate (%)",
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_inf, use_container_width=True)

# Chart 3: Treasury Yields
st.markdown("### US Treasury Yield Curve")
yields_data = {}
for code in ['DGS1', 'DGS3', 'DGS5', 'DGS7', 'DGS10', 'DGS30']:
    try:
        yield_series = get_treasury_yields().get(code, pd.Series())
        if not yield_series.empty:
            yields_data[code.replace('DGS', 'Y')] = yield_series
    except:
        pass

if yields_data:
    fig_yields = go.Figure()
    for name, series in yields_data.items():
        fig_yields.add_trace(go.Scatter(
            x=series.index,
            y=series,
            mode='lines',
            name=f"{name}Y {series.iloc[-1]:.2f}%",
            line=dict(width=2)
        ))
    fig_yields.update_layout(
        title="US Treasury Yield Curve",
        xaxis_title="Date",
        yaxis_title="Yield (%)",
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_yields, use_container_width=True)

# Chart 4: US Dollar Index
st.markdown("### USD Index (DXY)")
try:
    dxy = get_stock_indices().get('US Dollar', pd.Series())
    if not dxy.empty:
        fig_dxy = go.Figure()
        fig_dxy.add_trace(go.Scatter(
            x=dxy.index,
            y=dxy,
            mode='lines+markers',
            line=dict(color='#1f77b4', width=2)
        ))
        fig_dxy.update_layout(
            title="US Dollar Index",
            xaxis_title="Date",
            yaxis_title="USD Index",
            height=350
        )
        st.plotly_chart(fig_dxy, use_container_width=True)
except:
    pass

# Chart 5: Oil Prices
st.markdown("### Oil Prices (WTI & Brent)")
oil_data = get_oil_prices()
if oil_data['WTI'] is not None and not oil_data['WTI'].empty:
    fig_oil = go.Figure()
    wti = oil_data['WTI']
    try:
        brent = oil_data['Brent']
        if brent is not None and not brent.empty:
            fig_oil.add_trace(go.Scatter(
                x=brent.index,
                y=brent,
                mode='lines+markers',
                name='Brent',
                line=dict(color='#d62728', width=2)
            ))
    except:
        pass
    fig_oil.add_trace(go.Scatter(
        x=wti.index,
        y=wti,
        mode='lines+markers',
        name='WTI',
        line=dict(color='#ff7f0e', width=2)
    ))
    fig_oil.update_layout(
        title="Crude Oil Prices ($/barrel)",
        xaxis_title="Date",
        yaxis_title="Price ($/barrel)",
        height=350
    )
    st.plotly_chart(fig_oil, use_container_width=True)

# =============================================================================
# DATA TABLES
# =============================================================================

st.subheader("📊 Economic Indicators Table")

# Create comprehensive data table
table_data = {
    'Region': [],
    'GDP Growth': [],
    'Inflation': [],
    '10Y Yield': [],
    'Stock Index': [],
}

for region in regions:
    table_data['Region'].append(region_labels[regions.index(region)])

    gdp_val = get_latest_value(data['gdp'][region])
    if gdp_val is not None:
        table_data['GDP Growth'].append(f"{gdp_val:+.1f}%")
    else:
        table_data['GDP Growth'].append('N/A')

    if region in data['inflation']:
        inf_val = get_latest_value(data['inflation'][region])
        if inf_val is not None:
            table_data['Inflation'].append(f"{inf_val:+.1f}%")
        else:
            table_data['Inflation'].append('N/A')
    else:
        table_data['Inflation'].append('N/A')

    yield_val = get_latest_value(data['10y_yield'])
    if yield_val is not None:
        table_data['10Y Yield'].append(f"{yield_val:.2f}%")
    else:
        table_data['10Y Yield'].append('N/A')

    # Stock index
    try:
        indices = get_stock_indices()
        for idx_name, idx_series in indices.items():
            if not idx_series.empty:
                try:
                    idx_val = round(idx_series.iloc[-1], 0)
                except:
                    idx_val = get_latest_value(idx_series)
                table_data['Stock Index'].append(f"{idx_val or idx_series.iloc[-1]:.0f}")
                break
    except:
        table_data['Stock Index'].append('N/A')

# Create styled DataFrame
df_table = pd.DataFrame(table_data)
# Highlight negative values
df_table['GDP Growth'] = df_table['GDP Growth'].apply(
    lambda x: f"<span style='color: green'>{x}</span>" if x and x[0] == '+' else f"<span style='color: red'>{x}</span>" if x else x
)
df_table['Inflation'] = df_table['Inflation'].apply(
    lambda x: f"<span style='color: green'>{x}</span>" if x and x[0] == '+' else f"<span style='color: red'>{x}</span>" if x else x
)
df_table['Stock Index'] = df_table['Stock Index'].apply(
    lambda x: f"<span style='color: green'>{x}</span>" if x and x[0] == '+' else f"<span style='color: red'>{x}</span>" if x else x
)

st.dataframe(
    df_table,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Region": st.column_config.TextColumn("Region", width="medium"),
        "GDP Growth": st.column_config.TextColumn("GDP Growth", width="medium"),
        "Inflation": st.column_config.TextColumn("Inflation", width="medium"),
        "10Y Yield": st.column_config.TextColumn("10Y Yield", width="medium"),
        "Stock Index": st.column_config.TextColumn("Index", width="medium"),
    }
)

# =============================================================================
# CORRELATION HEATMAP
# =============================================================================

st.subheader("🔗 Regional Correlations")

# Calculate correlations from available data
correlations = {}
if gdp_comparison:
    # Transpose and calculate correlation
    df_gdp = pd.DataFrame(gdp_comparison)
    corr = df_gdp.corr()
    fig_corr = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu',
        colorbar=dict(title='Correlation'),
        hoverongaps=False
    ))
    fig_corr.update_layout(
        title="GDP Growth Correlations",
        height=350
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.caption("""
**Data Sources:** FRED, Yahoo Finance, World Bank, IMF\n
**Auto-refresh:** Enabled | **Refresh Interval:** {} | **Cached:** {}\n
""".format(
    REFRESH_INTERVALS['default'] // 60 if AUTO_REFRESH_ENABLED else "Manual",
    "Yes" if AUTO_REFRESH_ENABLED else "No"
))

# =============================================================================
# REAL-TIME UPDATES
# =============================================================================

# Auto-refresh loop (if enabled)
if auto_refresh:
    st.caption("🔄 Updating data...")
    for _ in range(60):  # Loop for 60 seconds to show updates
        time.sleep(REFRESH_INTERVALS['default'] // 60)  # Sleep for refresh interval
        try:
            # Force update oil prices periodically
            oil_data = get_oil_prices()
            if oil_data['WTI'] is not None and not oil_data['WTI'].empty:
                data['oil'] = oil_data['WTI']
        except:
            pass
