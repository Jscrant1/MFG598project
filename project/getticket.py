
import yfinance as yf

# this will gather the info from the ticker 
def getname(ticker):
    try:
        company_info = yf.Ticker(ticker)
        company_name = company_info.info['longName']
    except:
        print('Company Search Unsuccessful')

    return company_name