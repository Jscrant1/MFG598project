from transformers import pipeline
from getnews import news

# use a specific Financian News Sentiment analysis
classifier = pipeline(model = 'mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis')  
def sentiment(paragraph):
    data = classifier(paragraph)
    return data