import requests
from datetime import datetime, date

def format_date(date_str):
    """ Convert a date string to the format 'YYYYMMDD' required by the NYT API. """
    return datetime.fromisoformat(date_str).strftime('%Y%m%d')

def news(company_name, start_date, end_date):
    # Your API key
    api_key = 'fLnsZ9hNgGf9xos2NwgqxpCWk9C6YOry'

    # News API endpoint
    url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'

    # Convert dates to the required format
    start_date = format_date(start_date)
    end_date = format_date(end_date)

    # Parameters for the API call
    params = {
        'q': company_name,
        'api-key': api_key,
        'begin_date': start_date,
        'end_date': end_date,
        'fl': 'headline,web_url,pub_date,lead_paragraph',  # Fields to return
        'fq' : 'news_desk:("Business")'
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data['response']['docs']
        for article in articles:
            published_date = datetime.strptime(article['pub_date'], '%Y-%m-%dT%H:%M:%S%z')
            #print(f"Title: {article['headline']['main']}\nURL: {article['web_url']}\nlead_paragraph: {article['lead_paragraph']}\n")
    else:
        print("Failed to fetch news")
    
    return articles

if __name__ == '__main__':
    companyname = 'Apple'
    start='2023-10-01'
    to='2023-11-13'
    news(companyname,start,to)