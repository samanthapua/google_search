from pytrends.request import TrendReq
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

btc_prices = pd.read_csv('./historical_btc_prices.csv', usecols=['Date', 'Close', 'Volume'])


def settings(lang, timezone, search_words, timeperiod):
    pytrends = TrendReq(hl=lang, tz=timezone)
    pytrends.build_payload(search_words, cat=0, timeframe=timeperiod)
    count_df = pytrends.interest_over_time()
    country_df = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
    related_query_df = pytrends.related_queries()
    return count_df, country_df, related_query_df


if __name__ == '__main__':
    count_df, country_df, related_query_df = settings('en-US', 360, ['Bitcoin', 'BTC'], 'today 5-y')
    count_df = count_df.reset_index()
    count_df.loc[:, 'average_interest'] = (count_df['Bitcoin'] + count_df['BTC']) / 2
    count_df['date'] = pd.to_datetime(count_df['date'])
    count_df = count_df[['date', 'average_interest']]
    btc_prices['Date'] = pd.to_datetime(btc_prices['Date'])
    data = pd.merge(count_df, btc_prices, left_on='date', right_on='Date', how='inner')

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(data['date'], data['average_interest'], color='blue')
    ax.set_ylabel('Average Interest')

    ax.plot(data['date'], data['Close'], color='green')
    ax.set_ylabel('BTC Price')

    # ax.plot(data['date'], data['Volume'], color='orange')
    # ax.set_ylabel('Volume')

    fig.suptitle('Average Interest, Price, and Volume Over Time')
    ax.set_xlabel('Date')

    # Adjust the layout
    fig.tight_layout()

    # Show the plot
    plt.show()

    'Geomap code'
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    country_df = country_df.reset_index()
    country_df = country_df[country_df['Bitcoin'] > 50]
    merged = world.merge(country_df, left_on='name', right_on='geoName')
    colors = [(0, 0.3, 0.6), (0.7, 0.8, 1), (1, 0.7, 0.7), (0.6, 0.2, 0)]
    cmap = LinearSegmentedColormap.from_list('my_cmap', colors, N=10)
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_title('Intensity of Google Searches on Bitcoin')
    merged.plot(column='Bitcoin', cmap=cmap, ax=ax, legend=True, vmin=50, vmax=100, edgecolor='white')

    for idx, row in merged.iterrows():
        if row['Bitcoin'] > 80:
            ax.annotate(row['name'], xy=row['geometry'].centroid.coords[0], ha='center', va='center', fontsize=5,
                        color='black', fontweight='bold')

    # plt.show()
