from fredapi import Fred
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
from dotenv import load_dotenv


plt.style.use('fivethirtyeight')
color_palette = plt.rcParams['axes.prop_cycle'].by_key()['color']

load_dotenv()
fred_key = os.getenv('fred_api_key')
fred = Fred(api_key=fred_key)
series = fred.get_series('RSXFSN')
df = pd.DataFrame(series, columns=['Value'])
df['Date'] = df.index
df = df.reset_index()
df['Date'] = pd.to_datetime(df['Date'])

# df=df.dropna()
# df['Month']=df['Date'].dt.to_period('M')
# plt.figure(figsize=(10,4))
# plt.plot(df['Date'],df['Value'],marker='o',linestyle='-')
# plt.title('Series:RSXFSN')
# plt.xlabel('Date')
# plt.ylabel('Value')
# plt.grid(True)
# plt.show()

unemp_results=fred.search('Unemployment Rate')
unrate=fred.get_series('UNRATE')
unrate.plot()
plt.show()