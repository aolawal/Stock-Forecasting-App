# Stock-Forecasting-App

# Stock Trend Analysis and Prediction with Prophet

# Problem Definition
### Investors are always in dilemma on the best stock to invest in, to maximize return on their investment. This was the rationale behind the project, to enable investor explore the profitability of investment options and make informed decision.

# The project aims to:
### 1. confirm the return on investment (ROI) on a stock with a view to determine its profitability by considering the ROI of the stock over a defined period
### 2. establish stock price movement by conducting a trend Analysis of Stock performance and forecasting future stock price using Facebook (FB) prophet.

# Data Preprocessing & Exploratory Data Analysis (EDA)
## Procedure:
### 1. The necessary libraries were imported
### 2. The timeframe of the data to be downloaded from Yahoo Finance was defined and the necessary Ticker symbol was inserted for loading
### 3. The datasets were pre-processed to prepare the data for analysis:
### 4. The datasets were imported from Yahoo Finance and aggregated into a dataframe
### 5. The index was reset, and the necessary data were extracted from the dataframe
### 6. The model was trained to fit the pre-processed data using FB Prophet
### 7. The model was evaluated to detect anomalies
### 8. The model was used to predict the price of selected stock using Matplotlib and FB prophet..


# Model Accuracy & Justification
### The accuracy of the model prediction of share price can be deduced by comparing the line chart showing the trend analysis of historical stock price movement (actual) of the selected vis a viz the trendline of the FB Prophet forecast. Ideally, FB prophet should be able to closely predict the pattern of share price movement except there are anomalies such as external shock that could result in either a decline or spike in share price (which should be further investigated). 

# Deployment Functionality & User Interface
### To ensure a friendly and robust user interface, streamlit was used to deploy the frontend of the model by integrating the app.py model with streamlit url on Github. 

## The app has a simple interactive interface whereby a user will perform the following 3 actions:
### 1.	select the country, stock and required timeframe of the stock of your choice
### 2.	select the number of days of forecast you want and
### 3.	run the forecast

## In return you will get the following output after clicking on the run the forecast button:
1.	Trend Analysis of the selected stock over the selected period
2.	The Return on Investment (ROI) of the stock over the selected time frame
3.	Share price information for the last 5 days
4.	Option to download the share price data for the selected time range
5.	Model Forecast trend chart covering selected timeframe and the near future
6.	FB prophet share price trend forecast (with option to zoom in and out over specific time frame)
7.	Option to download the share price forecast data for the selected time range

[Stock App Link](https://lawalstock-forecasting-app-blua22salmsjry2u5cdtjz.streamlit.app)

# Report & Code Quality
The code and the data is of high quality, the data is extracted from the website of a reputable and reliable organisation (Yahoo Finance).

Several tests had also been carried out on user interface interactivity before deciding on this final outcome. The codes are also flexible and universal; it gives users a wide array of options and flexibility in terms of being able to select a share and country of your choice and getting the required output. In addition, users have the option to download both historical and forecasted share price.
