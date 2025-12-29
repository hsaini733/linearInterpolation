import pandas as pd
import numpy as np
import requests

def generate_ms_data_from_hourly(symbol):
    # 1. Get the Data
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?range=3mo&interval=1h"
    headers = {'User-Agent': 'Mozilla/5.0'}
    data = requests.get(url, headers=headers).json()
    
    # 2. Extract price and time
    res = data['chart']['result'][0]
    timestamps = pd.to_datetime(res['timestamp'], unit='s')
    prices = res['indicators']['quote'][0]['close']
    
    # Create initial Hourly DataFrame
    df = pd.DataFrame({'price': prices}, index=timestamps)
    df = df.dropna() # Clean missing Yahoo data

    # 3. UPSAMPLE to 1000 Milliseconds (ms)(1s)
    # This creates a row for every single 1000MS between start and end
    df_ms = df.resample('1000ms').asfreq()
    
    # 4. INTERPOLATE the gaps
    # 'linear' draws a straight line between the hourly prices
    df_ms['price'] = df_ms['price'].interpolate(method='linear')
    
    # 5. GENERATE Synthetic Bid/Ask (Back-end logic)
    # We add/subtract 0.01% as a realistic spread for T.TO
    spread = 0.0005 
    df_ms['bid'] = df_ms['price'] * (1 - spread)
    df_ms['ask'] = df_ms['price'] * (1 + spread)
    
    # Add some "Jitter" so it looks real (Low Latency simulation)
    jitter = np.random.normal(0, 0.0001, len(df_ms))
    df_ms['price'] += jitter

    return df_ms

# Execute and show first 500ms
ms_data = generate_ms_data_from_hourly("T.TO")
print(ms_data.head(500))

# Save to Time Series CSV
ms_data.to_csv("T_TO_interpolated_ms.csv")