"""
Dashboard Configuration
"""
import os

# =============================================================================
# AUTO REFRESH INTERVALS (seconds)
# =============================================================================

REFRESH_INTERVALS = {
    'oil': 300,      # 5 minutes - oil prices change frequently
    'yields': 3600,  # 1 hour - bond yields update less frequently
    'gdp': 86400,    # 24 hours - GDP data is monthly/quarterly
    'inflation': 86400,  # 24 hours - CPI data is monthly
    'stocks': 3600,  # 1 hour - indices update daily
    'currencies': 600,    # 10 minutes - FX rates update frequently
    'crypto': 180,      # 3 minutes - crypto is highly volatile
    'default': 3600,    # 1 hour default
}

# Enable auto-refresh
AUTO_REFRESH_ENABLED = True
AUTO_REFRESH_DEFAULT = 3600  # 1 hour

# =============================================================================
# CHART SETTINGS
# =============================================================================

CHART_SIZES = {
    'small': (400, 300),   # Gauge, small comparison charts
    'medium': (600, 400),  # Standard charts
    'large': (800, 500),   # Main dashboard charts
}

CHART_COLORS = {
    'US': {'primary': '#1f77b4', 'secondary': '#1f77b4'},
    'Eurozone': {'primary': '#ff7f0e', 'secondary': '#ff7f0e'},
    'China': {'primary': '#2ca02c', 'secondary': '#98df8a'},
    'Japan': {'primary': '#d62728', 'secondary': '#ff9896'},
    'UK': {'primary': '#9467bd', 'secondary': '#c5b0d5'},
    'EM': {'primary': '#8c564b', 'secondary': '#c49c94'},
}

# =============================================================================
# DATA SOURCE SETTINGS
# =============================================================================

DATA_SOURCES = {
    'gdp': {
        'US': 'fred://GDPC1',
        'EU': 'fred://FE_GDP_EU',
        'China': 'wb://CN/NY.GDP.MKTP.KD.ZG',
        'Japan': 'fred://JPGDP',
        'UK': 'fred://UKGDPC',
        'EM': 'api://IMF/EM_GDP',
    },
    'inflation': {
        'US': 'fred://CPIAUCSL',
        'EU': 'fred://FE_PCE_EU',
        'China': 'fred://CHINCPI',
        'Japan': 'fred://JPCPIALLSL',
        'UK': 'fred://UKNFCPI',
    },
    'unemployment': {
        'US': 'fred://UNRATE',
    },
    'treasury': {
        'US_1Y': 'fred://DFG1',
        'US_5Y': 'fred://DFG5',
        'US_10Y': 'fred://DGS10',
        'US_30Y': 'fred://DFG30',
    },
    'stocks': {
        'US_SP500': 'yf://^GSPC',
        'US_NASDAQ': 'yf://^IXIC',
        'Euro': 'yf://STOXX50E',
        'Germany': 'yf://^GDAXI',
        'Japan': 'yf://^N225',
        'China': 'yf://000001.SS',
        'UK': 'yf://^FTSE',
    },
    'oil': {
        'WTI': 'yf://CL=F',
        'Brent': 'yf://BZ=F',
        'LNG': 'yf://NG=F',
    },
    'crypto': {
        'Bitcoin': 'yf://BTC-USD',
        'Ethereum': 'yf://ETH-USD',
    },
}

# =============================================================================
# DASHBOARD LAYOUT
# =============================================================================

DASHBOARD_WIDTH = 'large'  # 'small', 'medium', 'large'
SIDEBAR_WIDTH = 'medium'   # 'small', 'medium', 'large'

# =============================================================================
# REGION METRICS
# ======================================================================

REGION_METRICS = {
    'US': ['GDP_growth', 'inflation', 'unemployment', 'yield_10y', 'sp500', 'dollar'],
    'Eurozone': ['GDP_growth', 'inflation', 'yield_10y', 'stoxx50', 'euro'],
    'China': ['GDP_growth', 'inflation', 'yield_10y', 'sse', 'cny'],
    'Japan': ['GDP_growth', 'inflation', 'yield_10y', 'nikkei', 'jpy'],
    'UK': ['GDP_growth', 'inflation', 'yield_10y', 'ftse', 'gbp'],
    'EM': ['GDP_growth', 'inflation', 'yield_10y', 'msci_em', 'em_fx'],
}

# =============================================================================
# THEME SETTINGS
# =============================================================================

THEME = {
    'primary_color': '#1f77b4',
    'secondary_color': '#2ca02c',
    'accent_color': '#ff7f0e',
    'bg_color': '#ffffff',
    'text_color': '#333333',
    'font_family': 'Inter, system-ui, sans-serif',
}

# =============================================================================
# API RATES
# =============================================================================

API_RATES = {
    'fred': None,           # No rate limit for basic series
    'yfinance': 10,         # 10 calls per second (soft limit)
    'oanda': 15,           # 15 calls per minute
}

# =============================================================================
# DATA HISTORY PERIODS
# =============================================================================

HISTORY_PERIODS = {
    'daily': '30d',
    'weekly': '1y',
    'monthly': '10y',
}
