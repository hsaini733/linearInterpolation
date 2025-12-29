Architecting a High-Frequency Financial Data Pipeline from Synthetic Micro-ticks



Overview



In the domain of low-latency financial systems, the availability of high-resolution data is often a significant barrier to entry. This project demonstrates a robust data engineering solution: transforming standard, low-frequency market data into a high-frequency synthetic stream for use in advanced financial modeling.



imagine getting 3 months of timeseries data from yahoo finance :



https://query2.finance.yahoo.com/v8/finance/chart/T.TO?range=3mo&interval=1s



This gives us : {

 "chart": {

  "result": null,

  "error": {

   "code": "Bad Request",

   "description": "Invalid input - interval=1s is not supported. Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 4h, 1d, 5d, 1wk, 1mo, 3mo]"

  }

 }

}





For predictability analysis for trading purpose we need timeseries data across all intervals may be every millisecond . Here I narrowed down how you can use linear interpolation to return hourly data and convert it to every second. This might not be 100% accurate but in the range of 80 to 90% accuracy except the volatile events .



The only way to get is hourly data :

https://query2.finance.yahoo.com/v8/finance/chart/T.TO?range=3mo&interval=1h



The primary objective was the conversion of sparse, hourly OHLC (Open-High-Low-Close) data from Yahoo Finance into a continuous, second-by-second time-series.

Temporal Resampling: Using the Pandas library, I upsampled historical hourly data to a 1,000ms (1-second) frequency grid.

Linear Interpolation: To bridge the gaps between hourly observations, I implemented a linear interpolation algorithm ($LERP$). This ensures a mathematically consistent price transition across the generated time steps.

Synthetic Bid/Ask Modeling: To simulate a live trading environment, I engineered a synthetic spread model. By applying a percentage-based offset to the interpolated price, the pipeline generates realistic liquidity indicators (Bid and Ask prices) essential for back-testing and UI visualization.

My main purpose of using it is to :



   1. Determine best and worst path for future performance using Monte Carlo Simulation.

   

   2. Using Traditional models such as ARIMA ....(more details by my former manager Aniket Hingane [https://www.linkedin.com/in/aniket-hingane-data-ai-ml/] here : [https://medium.com/@learn-simplified/build-arima-model-from-scratch-part-1-b72b73ba230f]

   

   3. Implement and test Prophet open source software released by Facebook’s Core Data Science team. It is available for download on CRAN and PyPI. [https://facebook.github.io/prophet/])



The below repo shows how I can use python to generate time series data for Telus (T.TO) for the last 3 months 



[https://github.com/hsaini733/linearInterpolation]

