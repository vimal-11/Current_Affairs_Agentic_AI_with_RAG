from newsapi import NewsApiClient
from utils import fetch_full_article, extract_article_content_from_xml, dict_to_xml


newsapi = NewsApiClient(api_key='ed79cabfc3c5467e85924626745833f7')


# /v2/everything - fetch from news api
all_articles = newsapi.get_everything(q='Isreal Iran',
                                      # sources='bbc-news,the-verge',
                                      # domains='bbc.co.uk,techcrunch.com',
                                      from_param='2025-06-10',
                                      language='en',
                                      sort_by='relevancy',
                                    )


# extract full content using url
for art in all_articles['articles']:
    full_text = fetch_full_article(art['url'])
    if full_text:
        art['full_content'] = full_text if full_text else "Not available"
    else:
        print("FULL CONTENT: Not available\n")
    # Ensure nested 'source' has 'id' field as string if None
    if 'source' in art and isinstance(art['source'], dict):
        if art['source'].get('id') is None:
            art['source']['id'] = 'None'


# Extract only the list of articles
articles_list = all_articles['articles']

# Convert to XML
xml_output = dict_to_xml(articles_list, root_name='articles', item_name='article')

# Save the pretty XML to a file.
file_name = "data/article.xml"
with open(file_name, "w", encoding="utf-8") as f:
    f.write(xml_output)
print(f"\nSuccessfully saved XML to {file_name}")

# Extract raw Content from XML
articles_content_data = extract_article_content_from_xml(file_name)

