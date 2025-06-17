from playwright.sync_api import sync_playwright
from newspaper import Article
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
from lxml import etree



# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()
#     page.goto("https://www.bbc.co.uk/news/articles/cjrld3erq4eo", timeout=60000)
#     page.wait_for_selector("main")  # wait for full article to load
#     content = page.locator("main").inner_text()
#     print(content)
#     browser.close()
    
    

def fetch_full_article(url):
    """
    Fetches and returns the full textual content of a news article from a given URL.
    
    Args:
        url (str): The URL of the article to fetch.
        
    Returns:
        str or None: The raw full text of the article or None if unsuccessful.
    """
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None
    



def dict_to_xml(data, root_name='root', item_name='item'):
    """
    Converts a dictionary or list of dictionaries to a pretty-printed XML string.
    
    Args:
        data (dict or list): The data to convert.
        root_name (str): The name of the root XML tag.
        item_name (str): The name to use for each item element (if data is a list).
        
    Returns:
        str: A pretty-printed XML string.
    """
    # Convert dict/list to XML bytes
    xml_bytes = dicttoxml(
        data,
        custom_root=root_name,
        item_func=lambda x: item_name,
        attr_type=False
    )
    # Decode to string
    xml_string = xml_bytes.decode('utf-8')
    dom = parseString(xml_string)
    pretty_xml = dom.toprettyxml()
    return pretty_xml




def extract_article_content_from_xml(xml_file_path):
    """
    Extracts full_content, title, and author from the XML file of articles using XPath.
    
    Args:
        xml_file_path (str): Path to the XML file.
        
    Returns:
        List[Dict]: A list of dictionaries, each with keys 'full_content', 'title', 'author'.
    """
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()
    
    # Parse XML content
    tree = etree.fromstring(xml_content.encode('utf-8'))
    articles = tree.xpath('//article')
    results = []
    for art in articles:
        # Use XPath to find elements inside each article
        full_content = art.xpath('.//full_content/text()')
        title = art.xpath('.//title/text()')
        author = art.xpath('.//author/text()')
        # Extract text or default to None
        title = title[0] if title else None
        author = author[0] if author else None
        full_content = full_content[0] if full_content else None
        
        results.append({
            'title': title,
            'author': author,
            'full_content': full_content,
        })
    
    return results
