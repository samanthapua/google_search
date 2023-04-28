from pytrends.request import TrendReq
import pandas as pd

btc_prices = pd.read_csv('./historical_btc_prices.csv',usecols=['Date','Close','Volume'])

def settings(lang,timezone,search_words,timeperiod):
    pytrends = TrendReq(hl=lang, tz=timezone)
    pytrends.build_payload(search_words,cat=0,timeframe=timeperiod)
    count_df = pytrends.interest_over_time()
    country_df = pytrends.interest_by_region(resolution='COUNTRY',inc_low_vol=True,inc_geo_code=False)
    related_query_df = pytrends.related_queries()
    return count_df, country_df, related_query_df

if __name__ == '__main__':
    count_df,country_df,related_query_df = settings('en-US',360,['Bitcoin','BTC'],'today 5-y')
    count_df = count_df.reset_index()
    count_df.loc[:, 'average_interest'] = (count_df['Bitcoin'] + count_df['BTC'])/2
    count_df['date'] = pd.to_datetime(count_df['date'])
    count_df = count_df[['date', 'average_interest']]
    btc_prices['Date'] = pd.to_datetime(btc_prices['Date'])
    print_df = pd.merge(count_df, btc_prices, left_on='date', right_on='Date',how='inner')

