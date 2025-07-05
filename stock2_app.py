import streamlit as st
import yfinance as yf
import datetime as dt
from prophet import Prophet
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import pandas as pd
import io

# Streamlit page config
st.set_page_config(page_title="Stock Forecast App", layout="wide")

# Dictionary of exchanges and currency mapping
exchange_suffixes = {
    "USA": ("", "USD"),
    "JAPAN": (".T", "JPY"),
    "INDIA": (".NS", "INR"),
    "UK": (".L", "GBP"),
    "FRANCE": (".PA", "EUR"),
    "GERMANY": (".DE", "EUR"),
    "CANADA": (".TO", "CAD"),
    "AUSTRALIA": (".AX", "AUD"),
    "HONG KONG": (".HK", "HKD"),
    "CHINA": (".SS", "CNY"),
    "SOUTH KOREA": (".KS", "KRW"),
    "SOUTH AFRICA": (".JO", "ZAR")
}

def download_data(country, ticker_base, start_date, end_date):
    country = country.upper()
    ticker_base = ticker_base.upper()
    if country not in exchange_suffixes:
        st.error(f"The stock exchange for '{country}' is not supported.")
        return None, None, None
    suffix, currency = exchange_suffixes[country]
    ticker = ticker_base + suffix
    data = yf.download(ticker, start=start_date, end=end_date)
    if data.empty:
        st.error(f"No data found for ticker '{ticker}'.")
        return None, None, None
    data.reset_index(inplace=True)
    return data, ticker, currency

def prepare_prophet_data(data):
    df = data[['Date', 'Close']].copy()
    df.columns = ['ds', 'y']
    return df

def forecast_stock(data, forecast_days=91):
    df_prophet = Prophet(changepoint_prior_scale=0.15,
                         yearly_seasonality=True,
                         daily_seasonality=True)
    df_prophet.fit(data)
    future = df_prophet.make_future_dataframe(periods=forecast_days, freq='D')
    forecast = df_prophet.predict(future)
    return df_prophet, forecast

def plot_price_trend(data, ticker, currency):
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(data['Date'], data['Close'], color='blue', label='Price')
    ax.set_title(f'{ticker} Price Trend')
    ax.set_xlabel('Date')
    ax.set_ylabel(f'Close Price ({currency})')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Download buttons
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button("📄 Download Price Trend CSV", csv, f"{ticker}_price_trend.csv", "text/csv")

    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png')
    st.download_button("🖼️ Download Price Trend Chart", img_buf.getvalue(), f"{ticker}_price_trend.png", "image/png")

def plot_forecast(df_prophet, forecast, ticker, currency):
    fig = df_prophet.plot(forecast, xlabel='Date', ylabel=f'{ticker} Stock Price ({currency})')
    plt.title(f'{ticker} Stock Price Forecast')
    st.pyplot(fig)

def plot_prediction_variance(data, forecast, ticker, currency):
    # Matplotlib chart
    fig1, ax1 = plt.subplots(figsize=(18, 7))
    ax1.plot(data['ds'], data['y'], label="Actual", linewidth=2, color='black')
    ax1.plot(forecast['ds'], forecast['yhat_lower'], label="Predicted lower", linewidth=2, color='green')
    ax1.plot(forecast['ds'], forecast['yhat_upper'], label="Predicted upper", linewidth=2, color='red')
    ax1.set_title(f'{ticker} Stock Price with Prediction Variance')
    ax1.set_xlabel('Date')
    ax1.set_ylabel(f'{ticker} Price ({currency})')
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

    # Plotly chart with date tooltips
    trace_actual = go.Scatter(name='Actual price', mode='markers',
        x=list(data['ds']), y=list(data['y']),
        marker=dict(color='black', line=dict(width=2)))
    trace_trend = go.Scatter(name='Trend', mode='lines',
        x=list(forecast['ds']), y=list(forecast['yhat']),
        line=dict(color='red', width=3))
    trace_upper = go.Scatter(name='Upper band', mode='lines',
        x=list(forecast['ds']), y=list(forecast['yhat_upper']),
        line=dict(color='#57b88f'), fill='tonexty')
    trace_lower = go.Scatter(name='Lower band', mode='lines',
        x=list(forecast['ds']), y=list(forecast['yhat_lower']),
        line=dict(color='#1705ff'))

    fig_plotly = go.Figure(data=[trace_actual, trace_trend, trace_lower, trace_upper])
    fig_plotly.update_layout(title=f'{ticker} Forecast using Prophet (Plotly)',
                             xaxis_title='Date', yaxis_title=f'{ticker} Price ({currency})')
    st.plotly_chart(fig_plotly, use_container_width=True)

def calculate_roi(data, ticker):
    start_price = float(data['Close'].iloc[0])
    end_price = float(data['Close'].iloc[-1])
    roi = ((end_price - start_price) / start_price) * 100
    st.markdown(f"### ROI for {ticker}: `{roi:.2f}%` from {data['Date'].iloc[0].date()} to {data['Date'].iloc[-1].date()}`")

# --- Streamlit UI ---
st.title("📈 Stock Forecasting App with Prophet")

# Sidebar
st.sidebar.header("User Inputs")
country = st.sidebar.selectbox("Select Stock Exchange Country", list(exchange_suffixes.keys()))
ticker_base = st.sidebar.text_input("Enter Ticker Symbol (e.g. AAPL)", "AAPL")
start_date = st.sidebar.date_input("Start Date", dt.date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", dt.date.today())
forecast_days = st.sidebar.slider("Forecast Days", min_value=30, max_value=365, value=91, step=30)

if st.sidebar.button("Run Forecast"):
    data, ticker, currency = download_data(country, ticker_base, start_date, end_date)
    if data is not None:
        st.subheader(f"Raw data for {ticker}")
        st.dataframe(data.tail())

        st.subheader("Price Trend")
        plot_price_trend(data, ticker, currency)

        calculate_roi(data, ticker)

        df_prophet_data = prepare_prophet_data(data)

        st.subheader("Forecast Plot (Prophet)")
        model, forecast = forecast_stock(df_prophet_data, forecast_days)
        plot_forecast(model, forecast, ticker, currency)

        st.subheader("Prediction Variance")
        plot_prediction_variance(df_prophet_data, forecast, ticker, currency)

        st.subheader("Forecast Data")
        forecast_display = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_days)
        st.dataframe(forecast_display)

        forecast_csv = forecast_display.to_csv(index=False).encode('utf-8')
        st.download_button("📄 Download Forecast CSV", forecast_csv, f"{ticker}_forecast.csv", "text/csv")
