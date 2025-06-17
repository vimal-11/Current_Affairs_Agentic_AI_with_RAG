from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='ed79cabfc3c5467e85924626745833f7')


# /v2/everything
all_articles = newsapi.get_everything(q='Apple',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2025-06-10',
                                    #   to='2025-06-17',
                                      language='en',
                                      sort_by='relevancy',
                                    #   page=2
                                    )

print(all_articles)