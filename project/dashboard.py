import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px

# these are custom scripts
from getticket import getname
import getnews
import sentimentanalysis
import getstocks 

app = Dash(__name__)

TITLE = html.H1(children='News Sentiment Analysis', style={'textAlign':'center'})

SYMBOLTITLE = html.H2(children='Ticker Symbol Selection')
symbolinput = dcc.Input(
    id = 'symbolinput',
    placeholder= 'Enter Ticker Symbol',
    type = 'text',
    value = '',
    debounce = True,
    )  
symbollist = dcc.Dropdown(
    id = 'symbollist',
    options = ['AAPL'], 
    multi = True
    )

companynames = html.Div(id = 'companynames')

DATERANGETITLE = html.H2(children = 'Select Range of Time for Prediction')
daterange = dcc.DatePickerRange(id = 'daterange',
                          min_date_allowed = date(2019,1,1),
                          max_date_allowed = date.today(),
                          initial_visible_month = date.today(),
                          end_date = date.today()
)

stocksplot = dcc.Graph(id='stocksplot'
                       )

SEARCHSTOCKBUTTON = html.Button(
    'Search Stocks',
    id = 'SEARCHSTOCKBUTTON',
    n_clicks = 0
)

GETNEWSBUTTON = html.Button(
    'Get News',
    id = 'GETNEWSBUTTON',
    n_clicks = 0
)

PREDICTIONTITLE = html.H2(children='Articles Perception Summary')
predictionmarkdown = dcc.Markdown(id = 'predictionmarkdown')

NEWSSTORIESTITLE = html.H2(children = 'News Stories and Their Perception')
newsstories = dcc.Markdown(id='newsstories', style={'white-space': 'pre-wrap'})

ERRORTITLE = html.H2(children='Error Box')
errorhandler = dcc.Input(
    id = 'errorhandler',
    value = '',
    readOnly = True
)

ARTICLEDATA = dcc.Store(id = 'ARTICLEDATA')

app.layout = html.Div([
    TITLE,
    SYMBOLTITLE,
    symbolinput,
    symbollist,
    companynames,
    
    # stocksplot,
    DATERANGETITLE,
    daterange,

    # SEARCHSTOCKBUTTON,
    GETNEWSBUTTON,

    
    PREDICTIONTITLE,
    predictionmarkdown,

    NEWSSTORIESTITLE,
    newsstories,



    ERRORTITLE,
    errorhandler,
    ARTICLEDATA,
])



#Updates the list of tickets with user inputted tickets
@callback(
    Output('symbollist','options'),
    Output('symbollist','value'),
    Output('symbolinput','value'),
    Output('errorhandler','value'),
    Input('symbolinput','value'),
    State('symbollist','options'),
    prevent_initial_call = True 
) 

def definesymbols(symbols, syms): #Auto populates the selection of tickets
    error = ''
    try:
        if symbols not in syms: #Make sure that there is not any overlap in tickets
            if len(symbols) <= 5:
                syms.append(symbols.upper())
            else:
                error = 'That is not a valid ticket'
    except:
        syms = []
        syms.append(symbols)
    return syms,syms,'',error 

#Allow the user to see which companies are being searched
@callback(
        Output('companynames','children'),
        Input('symbollist','value',),
        prevent_initial_call =True
)

def listcompanies(options):
    companyname = []
    for option in options:
        try:
            companyname.append(getname(option))
        except:
            print('Not a known company')
    return f'The companies being searched are {companyname}'

@callback(
    Output('newsstories', 'children'),
    Output('ARTICLEDATA', 'data'),
    Input('GETNEWSBUTTON','n_clicks'),
    State('daterange','start_date'),
    State('daterange','end_date'),
    State('symbollist','value'),
    prevent_initial_call =True
    
)
def news(click, start, end, symbols):
    displist = []
    infodict = {}
    for symbol in symbols: 
        artlist = []
        sentsum = {'Negitive' : 0,
               'Positive' : 0,
               'Neutral' : 0} # Reset the sentiment summary for each of the symbols 
        name = getname(symbol)
        articles = getnews.news(name, start, end)
        for article in articles:
            sent = sentimentanalysis.sentiment(article['lead_paragraph'])
            # Parse the date from the article
            published_date = datetime.strptime(article['pub_date'], '%Y-%m-%dT%H:%M:%S%z')
            
            # Format the date to a more readable form, e.g., "November 27, 2023"
            formatted_date = published_date.strftime('%B %d, %Y')
            article['sentiment'] = sent
            article['date'] = formatted_date
            disp = f"""
                    **Title:** {article['headline']['main']}
                    **URL:** [{article['web_url']}]({article['web_url']})
                    **Published:** {formatted_date}
                    **Lead Paragraph:** {article['lead_paragraph']}
                    **Sentiment:** {sent[0]['label']} with probability {sent[0]['score']:.4f}

                    ---
                    """
            # Update sentiment summary
            label = sent[0]['label'].capitalize()  # Capitalize to match keys in sentsum
            if label in sentsum:
                sentsum[label] += 1
            artlist.append(article) # append the data from the articles
            displist.append(disp) # Append a list of discriptions for easy interpertation 
        artlist.append(sentsum) # The last entry in the article list is always the sentiment summary 
        infodict.update({name : artlist})
    return displist, infodict

@callback(
    Output('predictionmarkdown', 'children'),    
    Input('ARTICLEDATA', 'data'),
    prevent_initial_call =True
)

def perceptionsummary(infodict):
    displst = []
    for key in infodict.keys():
        print(infodict[key][-1])
        disp = f"""
                **{key}** has a sentiment breakdown of {infodict[key][-1]}
        """
        displst.append(disp)
    return displst

# @callback(
#     Output('stocksplot','figure'),
#     Input('SEARCHSTOCKBUTTON', 'n_clicks'),
#     Input('GETNEWSBUTTON','n_clicks'),
#     State('daterange','start_date'),
#     State('daterange','end_date'),
#     State('symbollist','value'),
# )

# def stockgraph(click1,click2,start,end,symbols):
      

if __name__ == '__main__':
    app.run(debug=True)