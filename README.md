# Economic Outlook Dashboard

A live, auto-refreshing Streamlit dashboard that tracks global economic indicators across multiple regions.

## 🌍 Regions Tracked

- 🇺🇸 United States
- 🇪🇺 Eurozone
- 🇨🇳 China
- 🇯🇵 Japan
- 🇬🇧 United Kingdom
- 🌎 Emerging Markets

## 📊 Metrics

- GDP Growth (YoY)
- Inflation (CPI)
- Unemployment Rate
- Treasury Yields (1Y/5Y/10Y/30Y)
- Stock Market Indices
- Oil Prices (WTI/Brent)
- Currency Rates
- Gold & Crypto Prices

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

## 🔄 Auto-Refresh

- Enable auto-refresh in sidebar
- Refresh intervals: 5 min, 10 min, 30 min, 1 hour
- Oil prices update every 5 minutes
- Bond yields update every hour
- Stock indices update daily

## 📁 Files

- `app.py` - Main Streamlit application
- `data_sources.py` - Data fetching functions
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies

## 🌐 Data Sources

| Source | Coverage | Rate Limit |
|--------|----------|-----------|
| **FRED** | US, EU, UK, Japan economic data | Unlimited |
| **Yahoo Finance** | Stock indices, oil, crypto | 10/sec |
| **World Bank** | International GDP data | No limit |

## 📡 Deployment Options

1. **Local Machine** (Recommended for development)
   - Run locally with `streamlit run app.py`
   - Access via localhost

2. **Streamlit Cloud** (Free hosting)
   - Push code to GitHub
   - Connect to Streamlit Cloud
   - Free tier available

3. **Other Platforms**
   - Render: https://render.com
   - Railway: https://railway.app
   - AWS/Azure: Full control

## ⚙️ Configuration

Edit `config.py` to customize:
- Refresh intervals
- Chart colors and sizes
- Data history periods
- Theme settings

## 📚 NotebookLM Integration

Optionally use data from your NotebookLM research:
- Enable "Use NotebookLM Sample Data" in sidebar
- Dashboard will use baseline data from institutional research
- Ideal for testing or presentation mode

## 🔒 Security Notes

- Never commit `.env` file to git
- API keys stored locally
- FRED data is public (no key needed)
- Yahoo Finance is free for personal use

## 📈 Features

- ✅ Live data updates
- ✅ Interactive Plotly charts
- ✅ Regional comparison cards
- ✅ Correlation heatmaps
- ✅ GDP, inflation, yields tracking
- ✅ Auto-refresh with caching
- ✅ Beautiful responsive design

## 🛠️ Troubleshooting

**Charts not loading?**
- Check internet connection
- Verify data sources are accessible
- Clear Streamlit cache: `st.cache_data`

**Data appears stale?**
- Enable auto-refresh in sidebar
- Check API rate limits
- Restart the app

**FRED API errors?**
- Basic series don't require API key
- For rate-limited endpoints, use cached data

## 📞 Support

For issues or feature requests, open a GitHub issue.

---

*Built with Streamlit and Plotly* 📊
